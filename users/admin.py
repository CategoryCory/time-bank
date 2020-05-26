from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm

CustomUser = get_user_model()


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    """
    add_fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('email', )}),
    )

    add_fieldsets = (
        (None, {'classes': ('wide', ), 'fields': {'username', 'email', 'password1', 'password2'}}),
    )
    """
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['email', 'username', 'first_name', 'last_name', 'is_approved', 'is_staff', ]
    list_editable = ['is_approved', ]
    fieldsets = (
        ('Account Information', {'fields': ('username', 'email', 'first_name', 'last_name',)}),
        ('Personal Information', {'fields': ('date_of_birth', 'biography',)}),
        ('Address', {'fields': ('address_street', 'address_city', 'address_state', 'address_zip',)}),
        ('Social Media', {'fields': ('social_facebook', 'social_twitter', 'social_instagram', 'social_linkedin',)}),
        ('Permissions',
         {'fields': ('is_active', 'is_approved', 'is_staff', 'is_superuser', 'groups', 'user_permissions',)}),
        ('Important Dates', {'fields': ('last_login', 'date_joined',)}),
    )


admin.site.register(CustomUser, CustomUserAdmin)
