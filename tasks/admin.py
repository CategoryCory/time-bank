from django.contrib import admin
# from django.db import models
# from django.forms import CheckboxSelectMultiple

from .models import Task


class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'task_type', 'status', 'expires_on', 'created_by', ]
    list_editable = ['status', ]
    list_filter = ['status', ]
    list_per_page = 25
    # formfield_overrides = {
    #     models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    # }


admin.site.register(Task, TaskAdmin)
