from django.contrib import admin
from hujan_ui.installers.models import Server, Inventory, GlobalConfig, AdvancedConfig, Deployment

admin.site.register(Server)
admin.site.register(Inventory)
admin.site.register(GlobalConfig)
admin.site.register(AdvancedConfig)
admin.site.register(Deployment)
