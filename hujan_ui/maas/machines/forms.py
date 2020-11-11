from django import forms
from hujan_ui.maas.utils import MAAS


class AddMachineForm(forms.Form):
    hostname = forms.CharField(label='Machine name')
    domain = forms.ChoiceField()
    ARCHITECTURE = [
        ('amd64/generic', 'amd64/generic'),
    ]
    architecture = forms.ChoiceField(choices=ARCHITECTURE)
    # minimum_kernel = forms.CharField()
    zone = forms.ChoiceField()
    resouce_pool = forms.ChoiceField()
    mac_addresses = forms.CharField(label='MAC Address')
    POWER_TYPE = [
        ('amt', 'Intel AMT'),
        ('apc', 'American Power Conversion (APC) PDU'),
        ('dli', 'Digital Loggers, Inc. PDU'),
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
    power_type = forms.ChoiceField(choices=POWER_TYPE, initial=POWER_TYPE[5][0])

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


class PowerTypeIPMIForm(forms.Form):
    DRIVER = [
        ('LAN_2_0', 'LAN_2_0 [IPMI 2.0]'),
        ('LAN', 'LAN [IPMI 1.5]'),
    ]
    power_driver = forms.ChoiceField(choices=DRIVER)
    BOOT_TYPE = [
        ('auto', 'Automatic'),
        ('legacy', 'Legacy boot'),
        ('efu', 'EFI boot'),
    ]
    power_boot_type = forms.ChoiceField(choices=BOOT_TYPE)
    power_address = forms.CharField()
    power_user = forms.CharField()
    power_pass = forms.CharField()
    mac_address = forms.CharField(label='Power MAC')


class PhysicalForm(forms.Form):
    name = forms.CharField()
    mac_address = forms.CharField()
    interface_speed = forms.CharField()
    link_speed = forms.IntegerField()


class CommissionForm(forms.Form):
    system_id = forms.CharField(required=True, widget=forms.TextInput({'type': 'hidden'}))
    enable_ssh = forms.BooleanField(required=False, label='Allow SSH access and prevent machine powering off')
    skip_bmc_config = forms.BooleanField(required=False, label='Skip configuring supported BMC controllers with a MAAS generated username and password')
    # dimatikan sementara karena membuat error
    # commissioning_scripts = forms.CharField(required=False, label='Additional commissioning scripts')
    skip_networking = forms.BooleanField(required=False, label='Retain network configuration')
    skip_storage = forms.BooleanField(required=False, label='Retain storage configuration')


class DeployForm(forms.Form):
    system_id = forms.CharField(required=True, widget=forms.TextInput(attrs={'type': 'hidden'}))


class ConfirmForm(forms.Form):
    system_id = forms.CharField(required=True, widget=forms.TextInput(attrs={'type': 'hidden'}))
