from django.db import models


class Server(models.Model):
    name = models.CharField(max_length=200)
    ip_address = models.CharField(max_length=100)
    description = models.CharField(max_length=220)
    system_id = models.TextField(help_text="unique id MAAS")

    def __str__(self):
        return self.name
