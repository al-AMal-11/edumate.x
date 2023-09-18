from django import forms
from .models import Class

class ClassSelectForm(forms.Form):
    class_name = forms.ModelChoiceField(
        queryset=Class.objects.all(),
        label='Select a class:',
        empty_label='-- Select --'
    )