from django import forms
from .models import Status


class CreateStatusForm(forms.ModelForm):

    class Meta:
        model = Status
        fields = ['name']
