from django import forms


class TaskRequestCreateForm(forms.Form):
    TYPE_CHOICES = [
        ('REQUEST', 'Request'),
        ('OFFER', 'Offer'),
    ]

    FREQUENCY_CHOICES = [
        ('ONE_TIME', 'One Time'),
        ('DAILY', 'Daily'),
        ('WEEKLY', 'Weekly'),
        ('BIWEEKLY', 'Biweekly'),
        ('MONTHLY', 'Monthly'),
        ('AS_NEEDED', 'As Needed'),
    ]

    title = forms.CharField()
    description = forms.CharField(widget=forms.Textarea)
    expires_on = forms.DateField()
    task_type = forms.ChoiceField(choices=TYPE_CHOICES)
    frequency = forms.ChoiceField(choices=FREQUENCY_CHOICES)
