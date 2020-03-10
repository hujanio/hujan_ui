from django import forms
from hujan_ui.maas.utils import MAAS


class AddDomainForm(forms.Form):
    name = forms.CharField()
    authoritative = forms.BooleanField(initial=True, required=False)

    def save(self):
        cleaned_data = super().clean()
        maas = MAAS()
        maas.post("domains/", data=cleaned_data)
