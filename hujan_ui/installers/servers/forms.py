from django import forms

from hujan_ui import maas
from hujan_ui.installers.models import Server


class AddServerForm(forms.Form):
    machine = forms.ChoiceField(label='Name')
    ip_address = forms.CharField(widget=forms.Select)
    description = forms.CharField(required=False, help_text="Short description from this server")
    system_id = forms.CharField()
    name = forms.CharField()

    def __init__(self, *args, **kwargs):
        self.machines = self.get_choices_machines()
        super().__init__(*args, **kwargs)
        self.fields['machine'].choices = self.machines
        self.fields['system_id'].widget = forms.HiddenInput()
        self.fields['name'].widget = forms.HiddenInput()

    def get_choices_machines(self):
        resp = maas.get_machines()
        return [
            (machine['system_id'], machine['fqdn']) for machine in resp
        ]

    def save(self):
        clean_data = super().clean()
        return Server.objects.create(
            name=clean_data['name'],
            ip_address=clean_data['ip_address'],
            description=clean_data['description'],
            system_id=clean_data['system_id']
        )
