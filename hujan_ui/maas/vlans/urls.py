from django.urls import path

from . import views

app_name = 'vlans'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:vlan_id>/detail/', views.detail, name='detail'),
]
