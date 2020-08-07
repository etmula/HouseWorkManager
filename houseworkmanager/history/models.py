from django.db import models

from django.utils.timezone import localdate

from django.utils import timezone


class Recode(models.Model):
    updated_at = models.DateTimeField(auto_now=True)
    date = models.DateField(default=localdate)
    executer = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='recodes')
    category = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    point = models.IntegerField()

    def __str__(self):
        return f'{self.date} {self.executer.username} {self.name}'