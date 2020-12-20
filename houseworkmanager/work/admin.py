from django.contrib import admin

from .models import Composite, Work, WorkExectedRecode, WorkUpdatedRecode

admin.site.register(Composite)
admin.site.register(Work)
admin.site.register(WorkExectedRecode)
admin.site.register(WorkUpdatedRecode)
