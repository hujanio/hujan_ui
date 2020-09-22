from django import forms

class SubnetForm(forms.Form):
    cidr = forms.CharField(required=True)
    name = forms.CharField(required=False)
    description = forms.CharField(required=False)
    vlan = forms.ChoiceField(required=False)
    fabric = forms.ChoiceField(required=False)
    vid = forms.ChoiceField(required=False)
    space = forms.CharField(required=False)
    gateway_ip = forms.CharField(required=False)

    RDNS= [
        (0,'Disabled'),
        (1,'Enabled'),
        (2,'RFC2317'),
    ]
    rdns_mode = forms.ChoiceField(choices=RDNS)
    allow_dns = forms.BooleanField()
    allow_proxy = forms.BooleanField()
    dns_servers = forms.CharField(required=False)
    managed = forms.IntegerField(required=False)