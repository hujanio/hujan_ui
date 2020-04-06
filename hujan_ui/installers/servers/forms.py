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


class EditServerForm(AddServerForm):
    def __init__(self, *args, **kwargs):
        self.id = kwargs['instance'].id
        super().__init__(*args, **kwargs)
        self.fields['machine'].initial = kwargs['instance'].system_id
        
    def save(self):
        clean_data = super().clean()
        server = Server.objects.get(id=self.id)
        server.name = clean_data['name']
        server.ip_address = clean_data['ip_address']
        server.description = clean_data['description']
        server.system_id = clean_data['system_id']
        return server.save()
        