from django.urls import path

from . import views

app_name = 'configurations'
urlpatterns = [
    path('global-config', views.global_config, name='global_config'),
]
