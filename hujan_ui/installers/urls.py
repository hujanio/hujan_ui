from django.urls import path, include

from . import views

app_name = 'installer'
urlpatterns = [
    path('servers/', include('hujan_ui.installers.servers.urls')),
    path('inventory', views.inventory, name='inventory'),
    path('global-config', views.global_config, name='global_config'),
    path('advanced-config', views.advanced_config, name='advanced_config'),
    path('deploy', views.deploy, name='deploy')
]
