from django import forms
from hujan_ui import maas
class SubnetForm(forms.Form):
    cidr = forms.CharField(required=True)
    name = forms.CharField(required=False)
    description = forms.CharField(required=False)
    vlan = forms.ChoiceField(required=False)
    fabric = forms.ChoiceField(required=False,widget=forms.HiddenInput)
    vid = forms.ChoiceField(required=False,widget=forms.HiddenInput)
    # space = forms.ChoiceField(required=False)
    gateway_ip = forms.CharField(required=False)

    RDNS= [
        (0,'Disabled'),
        (1,'Enabled'),
        (2,'RFC2317'),
    ]
    rdns_mode = forms.ChoiceField(choices=RDNS)
    allow_dns = forms.BooleanField()
    allow_proxy = forms.BooleanField()
    # dns_servers = forms.CharField(required=False)
    # managed = forms.IntegerField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['vlan'].choices = self.get_choice_vlan()
        # self.fields['space'].choices = self.get_choice_space()
        
    
    def get_choice_vlan(self):
        resp = maas.get_vlans()
        b = [(i['id'], i['name']+' - '+ i['fabric']) for i in resp]
        b.insert(0,(None,'-------'))
        return b

    def get_choice_space(self):
        resp = maas.get_spaces()
        b = [(i['id'], i['name']) for i in resp]
        b.insert(0,(None,'-------')) 
        return b
            
        