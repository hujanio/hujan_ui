from django import forms

from hujan_ui import maas
from hujan_ui.installers.models import Server


class AddServerForm(forms.Form):
    name = forms.ChoiceField()
    ip_address = forms.CharField()
    description = forms.CharField(required=False, help_text="Short description from this server")
    system_id = forms.CharField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].choices = self.get_choices_machines()
        self.fields['ip_address'].widget.attrs['readonly'] = True
        self.fields['ip_address'].widget.attrs['placeholder'] = "IP Address"
        self.fields['system_id'].widget = forms.HiddenInput()

    def get_choices_machines(self):
        resp = maas.get_machines()
        return [
            (machine['fqdn'], machine['fqdn']) for machine in resp
        ]

    def save(self):
        clean_data = super().clean()
        return Server.objects.create(
            name=clean_data['name'],
            ip_address=clean_data['ip_address'],
            description=clean_data['description'],
            mechine=clean_data['system_id']
        )
