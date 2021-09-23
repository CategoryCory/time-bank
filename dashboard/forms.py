from django import forms
from django.contrib.auth import get_user_model
from django.forms import widgets

CustomUser = get_user_model()


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = (
            'first_name', 'last_name', 'username', 'date_of_birth', 'biography', 'skill_categories', 'skills', 
            'social_facebook', 'social_twitter', 'social_instagram', 'social_linkedin', 'profile_pic',
        )
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }
        help_texts = {
            'skill_categories': 'Hold CTRL (CMD on Mac) to select multiple skill categories'
        }