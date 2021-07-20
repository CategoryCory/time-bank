from django.contrib import admin

from .models import UserMessage


class UserMessageAdmin(admin.ModelAdmin):
    list_display = ['sender', 'recipient', 'job', 'timestamp', 'status', ]
    list_filter = ['sender', 'recipient', 'job', ]
    list_per_page = 25


admin.site.register(UserMessage, UserMessageAdmin)
