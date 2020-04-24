from django import forms

from hujan_ui.installers.models import GlobalConfig


class GlobalConfigForm(forms.ModelForm):

    class Meta:
        model = GlobalConfig
        fields = ('__all__')
        