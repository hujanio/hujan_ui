from django import forms
from hujan_ui.maas.utils import MAAS


class AddMachineForm(forms.Form):
    machine_name = forms.CharField()
    domain = forms.ChoiceField()
    ARCHITECTURE = [
        ('amd64/generic', 'amd64/generic'),
    ]
    architecture = forms.ChoiceField(choices=ARCHITECTURE)
    minimum_kernel = forms.CharField()
    zone = forms.ChoiceField()
    resouce_pool = forms.ChoiceField()
    mac_address = forms.CharField()
    POWER_TYPE = [
        ('amt', 'Intel AMT'),
        ('apc', 'American Power Conversion (APC) PDU'),
        ('dli', 'Digital Loggers, Inc. PDU'),
        ('fence_cdu', 'Sentry Switch CDU'),
        ('fence_cdu', 'Sentry Switch CDU'),
        ('hmc', 'IBM Hardware Management Console (HMC)'),
        ('ipmi', 'IPMI'),
        ('moonshot', 'HP Moonshot - iLO4 (IPMI)'),
        ('mscm', 'HP Moonshot - iLO Chassis Manager'),
        ('msftocs', 'Microsoft OCS - Chassis Manager'),
        ('nova', 'OpenStack Nova'),
        ('nova', 'OpenStack Nova'),
        ('openbmc', 'OpenBMC Power Driver'),
        ('recs_box', 'Christmann RECS|Box Power Driver'),
        ('redfish', 'Redfish'),
        ('smk15k', 'SeaMicro 15000'),
        ('ucsm', 'Cisco UCS Manager'),
        ('virsh', 'Virsh (virtual systems)'),
        ('vmware', 'VMware'),
        ("wedge", "Facebook's Wedge"),
        ("rsd", "Rack Scale Design"),
        ('vmware', 'VMware'),
    ]
    power_type = forms.ChoiceField(choices=POWER_TYPE)

    def __init__(self, *args, **kwargs):
        self.maas = MAAS()
        super().__init__(*args, **kwargs)
        self.fields['domain'].choices = self.get_choices_domains()
        self.fields['zone'].choices = self.get_choices_zones()
        self.fields['resouce_pool'].choices = self.get_choices_resourcepools()

    def get_choices_zones(self):
        resp = self.maas.get(f"/zones/").json()
        return [
            (zone['name'], zone['name']) for zone in resp
        ]

    def get_choices_domains(self):
        resp = self.maas.get(f"/domains/").json()
        return [
            (domain['name'], domain['name']) for domain in resp
        ]

    def get_choices_resourcepools(self):
        resp = self.maas.get(f"/resourcepools/").json()
        return [
            (resource['name'], resource['name']) for resource in resp
        ]
    