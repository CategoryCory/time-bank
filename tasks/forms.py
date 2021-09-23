from django import forms
from django.forms import widgets
from django.forms.models import inlineformset_factory
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, Div, HTML, ButtonHolder, Submit

from . import models
from .custom_layout_object import Formset


class TaskForm(forms.ModelForm):
    class Meta:
        model = models.Task
        exclude = ('created_by', 'status', )
        widgets = {
            'expires_on': forms.DateInput(attrs={'type': 'date'}),
        }
        help_texts = {
            'categories': 'Hold CTRL (CMD on Mac) to select multiple categories'
        }


class TaskAvailabilityForm(forms.ModelForm):

    class Meta:
        model = models.TaskAvailability
        exclude = ()


TaskAvailabilityFormSet = inlineformset_factory(
    models.Task,
    models.TaskAvailability,
    form=TaskAvailabilityForm,
    fields=['availability_day', 'availability_time', ],
    extra=7,
    can_delete=True,
)
