from django.db import models
from django.urls import reverse


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
            return reverse("work:work_detail", kwargs={"pk": self.head.pk})
        else:
            return reverse('work:workcommmit_create', kwargs={'pk': self.pk})
    
    def make_exucution_rate_dict(self):
        recodes = []
        for commit in self.commits.all():
            for recode in commit.recodes.all():
                recodes.append(recode)
        users = self.users
        execution_rate_dict = {user.username:0 for user in self.category.group.users.all()}
            
        for recode in recodes:
            for executer in recode.executers:
                if executer in recode.execution_rate_dict.keys():
                    execution_rate_dict[executer] += 1

        return count_dict
    
    def build_execution_rate_table(self):
        startdate = datetime(year, month, 1)
        enddate = datetime(year, month, calendar.monthrange(year, month)[1])
        users = self.users.all()
        table = [['work_name',] + [user.username for user in users],]
        point_dict = self.make_point_dict(startdate, enddate)
        for key, value in point_dict.items():
            row = [key.name,]
            for user in users.all():
                row.append(value[user.username])
            table.append(row)
        return table
    

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
