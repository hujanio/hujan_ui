from django.contrib import admin
from hujan_ui.installers.models import Server, Inventory, GlobalConfig


admin.site.register(Server)
admin.site.register(Inventory)
admin.site.register(GlobalConfig)
