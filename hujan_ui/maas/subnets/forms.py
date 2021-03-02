from django import forms
from hujan_ui import maas
from django.utils.translation import ugettext_lazy as _


class SubnetAddForm(forms.Form):
    name = forms.CharField(required=False)
    cidr = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Use IPv4 or IPv6'}))
    gateway_ip = forms.CharField(required=False)
    dns_servers = forms.CharField(required=False)
    vlan = forms.ChoiceField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['vlan'].choices = self.get_choice_vlan()
        # TODO: temporary comment because field space not used
        # self.fields['space'].choices = self.get_choice_space()

    def get_choice_vlan(self):
        resp = maas.get_vlans()
        choices = [(i['id'], i['fabric'] + ' - ' + i['name']) for i in resp]
        choices.insert(0, (None, '-------'))
        return choices


class SubnetForm(forms.Form):
    name = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Name (Optional)'}))
    cidr = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Use IPv4 or IPv6'}))
    gateway_ip = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Use IPv4 or IPv6 (Optional)'}))
    dns_servers = forms.CharField(required=False)
    description = forms.CharField(required=False)
    managed = forms.IntegerField(required=False)
    allow_proxy = forms.BooleanField(label=_('Proxy Access'))
    allow_dns = forms.BooleanField(label=_('Allow DNS Resolution'))
    vlan = forms.ChoiceField(required=False)
    fabric = forms.ChoiceField(required=False, widget=forms.HiddenInput)
    vid = forms.ChoiceField(required=False, widget=forms.HiddenInput)
    # TODO: commented temporarily or will be deleted because it is not used
    # space = forms.CharField(required=False, widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['vlan'].choices = self.get_choice_vlan()
        # TODO: temporary comment because field space not used
        # self.fields['space'].choices = self.get_choice_space(

    def get_choice_vlan(self):
        resp = maas.get_vlans()
        b = [(i['id'], i['name']+' - ' + i['fabric']) for i in resp]
        b.insert(0, (None, '-------'))
        return b

    def get_choice_space(self):
        resp = maas.get_spaces()
        b = [(i['id'], i['name']) for i in resp]
        b.insert(0, (None, '-------'))
        return b
