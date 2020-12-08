from datetime import datetime
import calendar

from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.shortcuts import reverse

from work.models import WorkExectedRecode


class CustomUserManager(UserManager):
    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):
        if not username:
            raise ValueError('The given username must be set')
        if not email:
            raise ValueError('The given email must be set')
        username = self.model.normalize_username(username)
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(username, email, password, **extra_fields)


class Group(models.Model):
    name = models.CharField(max_length=50)
    owner = models.OneToOneField(
        'User',
        related_name='own_group',
        on_delete=models.PROTECT,
    )

    def __str__(self):
        return self.name

    def get_works(self):
        works = []
        for category in self.categorys.all():
            works.extend([work for work in category.works.all()])
        return works

    def get_absolute_url(self):
        return reverse("accounts:group_detail", kwargs={"pk": self.pk})

    def make_point_dict(self, startdate, enddate):
        workexectedrecodes = WorkExectedRecode.objects.filter(
            group=self,
            exected_date__range=[startdate, enddate]
        )
        users = self.users
        point_dict = {}

        for workexectedrecode in workexectedrecodes:
            if workexectedrecode.workcommit not in point_dict.keys():
                point_dict[workexectedrecode.workcommit] = {
                    user.username: 0 for user in users.all()
                }
            for executer in workexectedrecode.executers.all():
                point_dict[workexectedrecode.workcommit][executer.username] += workexectedrecode.workcommit.point

        return point_dict

    def make_count_dict(self, startdate, enddate):
        workexectedrecodes = WorkExectedRecode.objects.filter(
            group=self,
            exected_date__range=[startdate, enddate]
        )
        users = self.users
        count_dict = {}

        for workexectedrecode in workexectedrecodes:
            if workexectedrecode.workcommit not in count_dict.keys():
                count_dict[workexectedrecode.workcommit] = {
                    user.username: 0 for user in users.all()
                }
            for executer in workexectedrecode.executers.all():
                count_dict[workexectedrecode.workcommit][executer.username] += 1

        return count_dict

    def build_point_table_monthly(self, year, month):
        startdate = datetime(year, month, 1)
        enddate = datetime(year, month, calendar.monthrange(year, month)[1])
        users = self.users.all()
        table = [['work_name', ] + [user.username for user in users], ]
        point_dict = self.make_point_dict(startdate, enddate)
        for key, value in point_dict.items():
            row = [key.name, ]
            for user in users.all():
                row.append(value[user.username])
            table.append(row)
        return table

    def build_count_table_monthly(self, year, month):
        startdate = datetime(year, month, 1)
        enddate = datetime(year, month, calendar.monthrange(year, month)[1])
        users = self.users.all()
        table = [['work_name', ] + [user.username for user in users], ]
        count_dict = self.make_count_dict(startdate, enddate)
        for key, value in count_dict.items():
            row = [key.name, ]
            for user in users:
                row.append(value[user.username])
            table.append(row)
        return table


class User(AbstractBaseUser, PermissionsMixin):
    """カスタムユーザーモデル."""
    username_validator = UnicodeUsernameValidator()

    group = models.ForeignKey('Group', related_name='users', on_delete=models.PROTECT, default=None, null=True, blank=True)

    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )

    email = models.EmailField(
        _('email address'),
        help_text=_('Required.')
    )
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = CustomUserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        """Return the first_name plus the last_name, with a space in
        between."""
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def calc_point(self, startdate=None, enddate=None, work=None):
        workexectedrecodes = self.workexectedrecodes
        if work:
            workexectedrecodes = workexectedrecodes.filter(work=work)
        if startdate:
            workexectedrecodes = workexectedrecodes.filter(
                exected_date__gte=startdate
            )
        if enddate:
            workexectedrecodes = workexectedrecodes.filter(
                exected_date__lte=enddate
            )

        points = 0
        for workexectedrecode in workexectedrecodes.all():
            points += workexectedrecode.point
        return points

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)
