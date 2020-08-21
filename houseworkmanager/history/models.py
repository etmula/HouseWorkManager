from datetime import datetime
import calendar
from collections import OrderedDict

from django.db import models
from django.utils.timezone import localdate
from django.utils import timezone
from django.urls import reverse


class Recode(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    exected_date = models.DateField(default=localdate)
    executers = models.ManyToManyField('accounts.User', related_name='recodes')
    workcommit = models.ForeignKey('work.WorkCommit', on_delete=models.PROTECT, related_name='recodes')
    group = models.ForeignKey('accounts.Group', on_delete=models.CASCADE, related_name='recodes')

    def __str__(self):
        return f'{self.exected_date} {[executer.username for executer in self.executers.all()]} {self.workcommit.name}'

    def get_absolute_url(self):
        return reverse("history:recode_detail", kwargs={"pk": self.pk})
