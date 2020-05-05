from django.db import models


class Server(models.Model):
    name = models.CharField(max_length=200)
    ip_address = models.CharField(max_length=100)
    description = models.CharField(max_length=220)
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
    ceph_pool_pg_num = models.CharField(max_length=30, default=30)
    ceph_pool_pgp_num = models.CharField(max_length=30, default=30)
    glance_backend_using_ceph = models.BooleanField(default=True)
    glance_backend_file = models.BooleanField(default=False)

    def __str__(self):
        return self.installation_type


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