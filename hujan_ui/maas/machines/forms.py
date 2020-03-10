from django import forms


class AddMachineForm(forms.Form):
    machine_name = forms.CharField()
    domain = forms.CharField()
    architecture = forms.CharField()
    minimum_kernel = forms.CharField()
    zone = forms.CharField()
    resouce_pool = forms.CharField()
    mac_address = forms.CharField()
    power_type = forms.CharField()
