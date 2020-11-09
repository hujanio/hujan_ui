from django import forms
from hujan_ui.maas.utils import MAAS


class FabricForm(forms.Form):
    name = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        self.maas = MAAS()
        super().__init__(*args, **kwargs)
