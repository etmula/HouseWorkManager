from django.db import models

from django.utils.timezone import localdate
from django.utils import timezone
from django.urls import reverse


class Recode(models.Model):
    updated_at = models.DateTimeField(auto_now=True)
    date = models.DateField(default=localdate)
    executer = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='recodes')
    category = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    point = models.IntegerField()
    group = models.ForeignKey('accounts.Group', on_delete=models.CASCADE, related_name='recodes')

    def __str__(self):
        return f'{self.date} {self.executer.username} {self.name}'

    def get_absolute_url(self):
        return reverse("history:recode_detail", kwargs={"pk": self.pk})
    