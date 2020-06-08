from django.contrib import admin
from .models import Requirement


class RequirementAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'is_active', )
    list_per_page = 25
    list_editable = ('is_active', )
    list_filter = ('is_active', )


admin.site.register(Requirement, RequirementAdmin)
