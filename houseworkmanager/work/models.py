from collections import deque

from django.db import models
from django.urls import reverse
from django.utils.timezone import localdate


class Composite(models.Model):
    group = models.ForeignKey(
        'accounts.Group',
        on_delete=models.CASCADE,
        related_name='composites'
    )
    name = models.CharField(max_length=20)
    parent = models.ForeignKey(
        'Composite',
        on_delete=models.CASCADE,
        related_name='composites',
        null=True,
        blank=True
    )

    def __str__(self):
        if self.parent:
            return f'{self.parent.__str__()}/{self.name}'
        else:
            return self.name

    def get_absolute_url(self):
        return reverse("work:composite_list", kwargs={'pk': self.id})

    def get_parents(self):
        path_list = deque()
        composite = self
        while composite.parent:
            path_list.appendleft(composite.parent)
            composite = composite.parent
        return path_list


class Work(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    group = models.ForeignKey(
        'accounts.Group',
        on_delete=models.CASCADE,
        related_name='works'
    )
    parent = models.ForeignKey(
        'Composite',
        on_delete=models.CASCADE,
        related_name='works',
        null=True,
        blank=True
    )
    name = models.CharField(max_length=30)
    point = models.IntegerField(default=0)
    description = models.TextField(blank=True, max_length=1000)
    alert = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, **kwargs):
        try:
            if self.point != Work.objects.get(id=self.id).point:
                WorkUpdatedRecode.objects.create(
                        updated_at=self.updated_at,
                        work=self,
                        name=self.name,
                        point=self.point
                    )
        except Work.DoesNotExist:
            pass
        return super(Work, self).save(**kwargs)

    def get_absolute_url(self):
        return reverse("work:work_detail", kwargs={"pk": self.pk})

    def get_latest_exected(self):
        return self.workexectedrecodes.latest('exected_date')


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
