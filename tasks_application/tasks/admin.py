# -*- coding: utf-8 *-*
from models import Task
from models import Project
from django.contrib import admin


class TaskAdmin(admin.ModelAdmin):
    radio_fields = {"project": admin.VERTICAL}

admin.site.register(Task, TaskAdmin)
admin.site.register(Project)
