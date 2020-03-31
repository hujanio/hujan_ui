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
