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
        print(self.head)
        if self.head:
            return reverse("work:work_detail", kwargs={"pk": self.pk})
        else:
            return reverse('work:workcommit_create', kwargs={'pk': self.pk})
    
    def last_exected_date(self):
        workcommits = self.commits.all()
        last_recode = Recode.objects.filter(
            workcommit__in=workcommits
        ).order_by('exected_date').last()
        return last_recode.exected_date
    

class WorkCommit(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    work = models.ForeignKey('Work', on_delete=models.CASCADE, related_name='commits')
    name = models.CharField(max_length=30)
    point = models.IntegerField(default=0)
    description = models.TextField(blank=True, max_length=1000)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("work:workcommit_detail", kwargs={"pk": self.pk})
