from django.db import models
from django.urls import reverse

class Category(models.Model):
    group = models.ForeignKey('accounts.Group', on_delete=models.CASCADE, related_name='categorys')
    name = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.name}'

class Work(models.Model):
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='works')
    name = models.CharField(max_length=30)
    point = models.IntegerField(default=0)
    description = models.TextField(blank=True, max_length=1000)
    alert = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("work:work_detail", kwargs={"pk": self.pk})
    