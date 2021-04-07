from django import forms
from django.forms.models import inlineformset_factory
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, Div, HTML, ButtonHolder, Submit

from . import models
from .custom_layout_object import Formset


class TaskForm(forms.ModelForm):

    # def __init__(self, *args, **kwargs):
    #     super(TaskForm, self).__init__(*args, **kwargs)
    #     self.helper = FormHelper()
    #     self.helper.form_tag = True
    #     self.helper.form_class = 'form-horizontal'
    #     self.helper.label_class = 'col-md-3 create-label'
    #     self.helper.field_class = 'col-md-9'
    #     self.helper.layout = Layout(
    #         Div(
    #             Field('title'),
    #             Field('description'),
    #             Field('expires_on'),
    #             Field('frequency'),
    #             # Field('categories'),
    #             Fieldset('When are you available?', Formset('availabilities')),
    #             HTML('<br>'),
    #             ButtonHolder(Submit('submit', 'Add Job')),
    #         )
    #     )

    class Meta:
        model = models.Task
        exclude = ('created_by', 'status', )


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
