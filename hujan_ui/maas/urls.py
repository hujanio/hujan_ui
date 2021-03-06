from django.urls import path, include

from . import views

app_name = 'maas'
urlpatterns = [
    path('machines/', include('hujan_ui.maas.machines.urls')),
    path('dns/', include('hujan_ui.maas.dns.urls')),
    path('subnets/', include('hujan_ui.maas.subnets.urls')),
    path('fabrics/', include('hujan_ui.maas.fabrics.urls')),
    path('spaces/', include('hujan_ui.maas.spaces.urls')),
    path('vlans/', include('hujan_ui.maas.vlans.urls')),
    path('settings/config_maas/', views.config_maas, name='config_maas'),
]
