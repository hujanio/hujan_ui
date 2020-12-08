from django import forms
from hujan_ui.installers.models import ConfigMAAS


class ConfigMAASForm(forms.ModelForm):
    
    class Meta:
        model = ConfigMAAS
        fields = ("__all__")
