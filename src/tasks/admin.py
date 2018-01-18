from django.contrib import admin

# Register your models here.
from .models import *


class TaskAdmin(admin.ModelAdmin):
    filter_horizontal = ('service_point',)


admin.site.register(Task, TaskAdmin)
