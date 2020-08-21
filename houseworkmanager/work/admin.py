from django.contrib import admin

from .models import Category, Work, WorkCommit

# Register your models here.

admin.site.register(Category)
admin.site.register(Work)
admin.site.register(WorkCommit)