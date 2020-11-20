from django.urls import path, include

from . import views

app_name = 'installer'
urlpatterns = [
    path('', views.index, name='index'),
    path('servers/', include('hujan_ui.installers.servers.urls')),
    path('inventories/', include('hujan_ui.installers.inventories.urls')),
    path('configurations/', include('hujan_ui.installers.configurations.urls')),
    path('global-config', views.global_config, name='global_config'),
    path('advanced-config', views.advanced_config, name='advanced_config'),
    path('deploy', views.deploy, name='deploy'),
    path('do_deploy', views.do_deploy, name='do_deploy'),
    path('deploy_log/<int:id>', views.deploy_log, name='deploy_log'),
    path('reset_all', views.reset_all, name='reset_all'),
    path('destroy', views.destroy_config, name='destroy_config'),
    path('post_deploy', views.post_deploy, name='post_deploy'),
]
