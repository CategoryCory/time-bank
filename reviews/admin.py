from django.contrib import admin

from .models import UserReview


class UserReviewAdmin(admin.ModelAdmin):
    list_display = ['rating', 'reviewee', 'author', 'created_on', ]
    list_per_page = 25


admin.site.register(UserReview, UserReviewAdmin)
