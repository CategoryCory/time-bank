from django.contrib import admin
# from django.db import models
# from django.forms import CheckboxSelectMultiple

from .models import Task, TaskResponse, TaskCategory, TaskAvailability


class TaskResponseInline(admin.TabularInline):
    model = TaskResponse
    extra = 0


class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'expires_on', 'created_by', ]
    list_editable = ['status', ]
    list_filter = ['status', ]
    list_per_page = 25
    inlines = [TaskResponseInline, ]
    # formfield_overrides = {
    #     models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    # }


class TaskCategoryAdmin(admin.ModelAdmin):
    pass


class TaskAvailabilityAdmin(admin.ModelAdmin):
    pass


admin.site.register(Task, TaskAdmin)
admin.site.register(TaskCategory, TaskCategoryAdmin)
admin.site.register(TaskAvailability, TaskAvailabilityAdmin)
