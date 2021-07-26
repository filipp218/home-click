from django.contrib import admin
from . import models


class TaskAdmin(admin.ModelAdmin):
    date_hierarchy = "date"
    list_filter = ["date"]


admin.site.register(models.Task, TaskAdmin)

