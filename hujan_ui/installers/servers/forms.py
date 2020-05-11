from django import forms

from hujan_ui import maas
from hujan_ui.installers.models import Server


class AddServerForm(forms.ModelForm):
    machine = forms.ChoiceField(label='Name')

    class Meta:
        model = Server
        fields = ['machine','ip_address', 'description', 'system_id', 'name']
        widgets = {
            'ip_address': forms.Select(),
            'description': forms.TextInput(attrs={'required': False}),
            'system_id': forms.HiddenInput(),
            'name': forms.HiddenInput()
        }
        help_texts = {
            'description': 'Short description from this server',
        }

    def __init__(self, *args, **kwargs):
        self.machines = self.get_choices_machines()
        super().__init__(*args, **kwargs)
        self.fields['machine'].choices = self.machines
        if self.instance.system_id:
            self.fields['machine'].initial = self.instance.system_id

    def get_choices_machines(self):
        resp = maas.get_machines()
        return [
            (machine['system_id'], machine['fqdn']) for machine in resp
        ]
