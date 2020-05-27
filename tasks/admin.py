from django.contrib import admin

from.models import Offer, Request


class OfferAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'expires', 'created_by', ]
    list_editable = ['status', ]
    list_filter = ['status', ]
    list_per_page = 25


class RequestAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'expires', 'created_by', ]
    list_editable = ['status', ]
    list_filter = ['status', ]
    list_per_page = 25


admin.site.register(Offer, OfferAdmin)
admin.site.register(Request, RequestAdmin)
