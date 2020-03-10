from django import forms
from django.utils.translation import ugettext_lazy as _

from hujan_ui.maas.utils import MAAS


class AddDomainForm(forms.Form):
    name = forms.CharField()
    authoritative = forms.BooleanField(initial=True, required=False)

    def save(self):
        cleaned_data = super().clean()
        maas = MAAS()
        return maas.post("domains/", data=cleaned_data)


class EditDomainForm(forms.Form):
    name = forms.CharField()
    authoritative = forms.BooleanField(initial=True, required=False)
    ttl = forms.CharField(
        label='TTL',
        required=False,
        help_text=_("if you want to use the default TTL, leave it blank")
    )

    def save(self, id):
        cleaned_data = super().clean()
        cleaned_data.update({'id': id})
        maas = MAAS()
        return maas.put(f"domains/{id}/", data=cleaned_data)
