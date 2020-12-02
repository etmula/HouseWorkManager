from django.db import models
from django.urls import reverse

from history.models import Recode


class Category(models.Model):
    group = models.ForeignKey('accounts.Group', on_delete=models.CASCADE, related_name='categorys')
    name = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse("work:category_detail", kwargs={"pk": self.pk})


class Work(models.Model):
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='works')
    head = models.ForeignKey('WorkCommit', on_delete=models.PROTECT, related_name='work_set', blank=True, null=True)
    alert = models.IntegerField(null=True, blank=True)

    def __str__(self):
        if self.head:
            return self.head.name
        else:
            return self.category.name

    def get_absolute_url(self):
        if self.head:
            return reverse("work:work_detail", kwargs={"pk": self.pk})
        else:
            return reverse('work:workcommit_create', kwargs={'pk': self.pk})
    
    def last_exected_date(self):
        workcommits = self.commits.all()
        last_recode = Recode.objects.filter(
            workcommit__in=workcommits
        ).order_by('exected_date').last()
        if last_recode:
            return last_recode.exected_date
        else:
            return None
    

class WorkExectedRecode(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    exected_date = models.DateField()
    executers = models.ManyToManyField(
        'accounts.User',
        related_name='workexectedrecodes'
    )
    work = models.ForeignKey(
        'Work',
        on_delete=models.SET_NULL,
        related_name='workexectedrecodes',
        null=True
    )
    group = models.ForeignKey(
        'accounts.Group',
        on_delete=models.CASCADE,
        related_name='workexectedrecodes'
    )
    name = models.CharField(max_length=30)
    point = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.exected_date} {[executer.username for executer in self.executers.all()]} {self.name}'

    def get_absolute_url(self):
        return reverse("work:workexectedrecode_detail", kwargs={"pk": self.pk})


class WorkUpdatedRecode(models.Model):
    updated_at = models.DateTimeField()
    work = models.ForeignKey(
        'Work',
        on_delete=models.CASCADE,
        related_name='workupdatedrecodes'
    )
    name = models.CharField(max_length=30)
    point = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.name}'
