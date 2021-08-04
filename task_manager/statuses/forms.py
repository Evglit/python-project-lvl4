from django import forms
from .models import Statuses


class Statuses(forms.Form):
    class Meta:
        model = Statuses
        fields = ['name']
