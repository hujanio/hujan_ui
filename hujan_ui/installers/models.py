from django.db import models

from multiselectfield import MultiSelectField
from model_utils import Choices


class Server(models.Model):
    name = models.CharField(max_length=200, unique=True)
    ip_address = models.CharField(max_length=100)
    description = models.CharField(max_length=220, blank=True)
    system_id = models.CharField(max_length=220, help_text="unique id MAAS")

    def __str__(self):
        return self.name


class Inventory(models.Model):
    server = models.ForeignKey(Server, on_delete=models.CASCADE)
    GROUP = (
        ('control', 'Controller'),
        ('network', 'Network'),
        ('compute', 'Compute'),
        ('monitoring', 'Monitoring'),
        ('storage', 'storage'),
    )
    group = models.CharField(max_length=50, choices=GROUP)

    class Meta:
        verbose_name = "inventory"
        verbose_name_plural = "inventories"

    def __str__(self):
        return f"{self.server} - {self.group}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)        
        Installer.set_step_inventory()


class GlobalConfig(models.Model):
    INSTALLATION_TYPE = (
        ('source', 'Source'),
    )
    installation_type = models.CharField(max_length=50, choices=INSTALLATION_TYPE, default='source')
    OPENSTACK_RELEASE = (
        ('train', 'Train'),
    )
    openstack_release = models.CharField(max_length=50, choices=OPENSTACK_RELEASE, default='train')
    internal_vip_address = models.CharField(max_length=30)
    external_vip_address = models.CharField(max_length=30)
    storage_interface = models.CharField(max_length=200)
    network_interface = models.CharField(max_length=200)
    neutron_plugin_agent = models.CharField(max_length=200)
    enable_tls_on_external_api = models.BooleanField(default=True)
    enable_ceph_service = models.BooleanField(default=True)
    enable_cinder_service = models.BooleanField(default=True)
    enable_magnum_service = models.BooleanField(default=True)
    enable_vpnaas = models.BooleanField(default=True)
    enable_fwaas = models.BooleanField(default=True)
    enable_qos = models.BooleanField(default=True)
    enable_ha_agent = models.BooleanField(default=True)
    enable_provider_networks = models.BooleanField(default=True)
    enable_port_forwading = models.BooleanField(default=True)
    enable_octavia_service = models.BooleanField(default=True)
    enable_promotheus_service = models.BooleanField(default=True)
    ceph_pool_pg_num = models.IntegerField(default=30)
    ceph_pool_pgp_num = models.IntegerField(default=30)
    glance_backend_using_ceph = models.BooleanField(default=True)
    glance_backend_file = models.BooleanField(default=False)

    def __str__(self):
        return self.installation_type

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)        
        Installer.set_step_global_config()


class AdvancedConfig(models.Model):
    SERVICE_TYPE = (
        ('octavia_service', 'Octavia Service'),
        ('neutron_service', 'Neutron Service'),
        ('ml2_plugin', 'ML2 Plugin'),
        ('heat_service', 'Heat Service'),
        ('magnum_service', 'Magnum Service'),
    )
    service_type = models.CharField(max_length=50, choices=SERVICE_TYPE)
    configuration = models.TextField()

    def __str__(self):
        return self.service_type


class Deployment(models.Model):
    DEPLOY_IN_PROGRESS = "in_progress"
    DEPLOY_SUCCESS = "success"
    DEPLOY_FAILED = "failed"
    DEPLOY_KOLLA = 'deploy_kolla'
    DEPLOY_POST_DEPLOY_SUCCESS = 'post_deploy_success'

    DEPLOY_STATUS = (
        (DEPLOY_IN_PROGRESS, "In Progress"),
        (DEPLOY_SUCCESS, "Success"),
        (DEPLOY_FAILED, "Failed"),
        (DEPLOY_KOLLA, "Deploy Kolla"),
        (DEPLOY_POST_DEPLOY_SUCCESS, "Deploy Success")
    )

    log_name = models.CharField(max_length=255)
    status = models.CharField(max_length=255, choices=DEPLOY_STATUS)

    @classmethod
    def get_status(cls):
        deployment = cls.objects.first()
        if deployment:
            return deployment.status
        return None


class Installer(models.Model):
    STEPS = Choices(
        ('server', 'Server'),
        ('inventory', 'Inventory'),
        ('global_configuration', 'Global Configuration'),
        ('advanced_configuration', 'Advanced Configuration'),
        ('deployment', 'Deployment'),
    )
    steps = MultiSelectField(choices=STEPS, default=STEPS.server)

    def __str__(self):
        return str(self.steps)

    @classmethod
    def get_steps(cls):
        installer = cls.objects.first()
        if not installer:
            installer = cls.objects.create()

        return installer.steps

    @classmethod
    def set_step_inventory(cls):
        installer = cls.objects.first()
        installer.steps.append(cls.STEPS.inventory)
        installer.save()
        return installer

    @classmethod
    def set_step_global_config(cls):
        installer = cls.objects.first()
        installer.steps.append(cls.STEPS.global_configuration)
        installer.save()
        return installer

    @classmethod
    def set_step_advanced_config(cls):
        installer = cls.objects.first()
        installer.steps.append(cls.STEPS.advanced_configuration)
        installer.save()
        return installer

    @classmethod
    def set_step_deployment(cls):
        installer = cls.objects.first()
        installer.steps.append(cls.STEPS.deployment)
        installer.save()
        return installer