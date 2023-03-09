from django import forms
from django.forms import TextInput

from labels.models import Label


class LabelForm(forms.ModelForm):
    class Meta:
        model = Label
        fields = ['name']
        widgets = {
            'name': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите название метки',
                'maxlength': '100'
            })
        }
