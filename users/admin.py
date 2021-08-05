from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import SkillCategory
# from tasks.models import Offer, Request

CustomUser = get_user_model()


class OfferInline(admin.TabularInline):
    pass
    # model = Offer
    # extra = 0


class RequestInline(admin.TabularInline):
    pass
    # model = Request
    # extra = 0


class SkillCategoryAdmin(admin.ModelAdmin):
    list_display = ['title', ]
    list_per_page = 25


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['email', 'username', 'first_name', 'last_name', 'is_approved', 'is_staff', ]
    list_editable = ['is_approved', ]
    list_filter = ['is_staff', 'is_superuser', 'is_active', 'is_approved', ]
    list_per_page = 25
    fieldsets = (
        ('Account Information', {'fields': ('username', 'email', 'first_name', 'last_name',)}),
        ('Personal Information', {'fields': ('date_of_birth', 'skill_categories', 'skills', 'biography', 'sullivan_coins_balance', 'profile_pic',)}),
        ('Address', {'fields': ('address_street', 'address_city', 'address_state', 'address_zip',)}),
        ('Social Media', {'fields': ('social_facebook', 'social_twitter', 'social_instagram', 'social_linkedin',)}),
        ('Permissions',
         {'fields': ('is_active', 'is_approved', 'is_staff', 'is_superuser', 'groups', 'user_permissions',)}),
        ('Important Dates', {'fields': ('last_login', 'date_joined',)}),
    )
    inlines = []


admin.site.register(SkillCategory, SkillCategoryAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
