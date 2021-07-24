from django.contrib import admin

from .models import UserMessageThread, UserMessage


class UserMessageInline(admin.TabularInline):
    model = UserMessage
    extra = 0


class UserMessageThreadAdmin(admin.ModelAdmin):
    list_display = ['created_by', 'recipient', 'job', 'created_on', ]
    list_filter = ['created_by', 'recipient', 'job', ]
    list_per_page = 25
    inlines = [UserMessageInline, ]


admin.site.register(UserMessageThread, UserMessageThreadAdmin)
