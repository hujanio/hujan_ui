from django.urls import path

from . import views

app_name = 'configurations'
urlpatterns = [
    path('global-config', views.global_config, name='global_config'),
    path('advanced-config', views.advanced_config, name='advanced_config'),
    path('add/', views.add_advanced_config, name='add_advanced_config'),
    path('edit/<int:id>', views.edit_advanced_config, name='edit_advanced_config'),
    path('delete/<int:id>', views.delete_advanced_config, name='delete_advanced_config'),
]
