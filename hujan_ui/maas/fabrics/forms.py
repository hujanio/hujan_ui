from django import forms
from hujan_ui.maas.utils import MAAS


class FabricForm(forms.Form):
    name = forms.CharField()
    description = forms.CharField()
    class_type = forms.CharField()

    def __init__(self, *args, **kwargs):
        self.maas = MAAS()
        super().__init__(*args, **kwargs)
