from django.contrib import admin
from django.db import models
from django.forms import CheckboxSelectMultiple

from.models import Offer, Request


class OfferAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'expires', 'created_by', ]
    list_editable = ['status', ]
    list_filter = ['status', ]
    list_per_page = 25
    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }


class RequestAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'expires', 'created_by', ]
    list_editable = ['status', ]
    list_filter = ['status', ]
    list_per_page = 25
    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }


class TagAdmin(admin.ModelAdmin):
    pass


admin.site.register(Offer, OfferAdmin)
admin.site.register(Request, RequestAdmin)
