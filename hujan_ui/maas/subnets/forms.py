from django import forms

class SubnetForm(forms.Form):
    cidr = forms.CharField()
    name = forms.CharField()
    description = forms.CharField()
    vlan = forms.ChoiceField()
    fabric = forms.ChoiceField()
    vid = forms.ChoiceField()
    space = forms.CharField()
    gateway_ip = forms.CharField()

    RDNS= [
        (0,'Disabled'),
        (1,'Enabled'),
        (2,'RFC2317'),
    ]
    rdns_mode = forms.ChoiceField(choices=RDNS)
    allow_dns = forms.BooleanField()
    allow_proxy = forms.BooleanField()
    dns_servers = forms.CharField()
    managed = forms.IntegerField()