from django.urls import path

app_name = 'vlans'
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.add, name='add'),
    path('<int:vlan_id>/edit/', views.edit, name='edit'),
    path('<int:vlan_id>/detail/', views.detail, name='detail'),
    path('<int:vlan_id/delete/', views.delete, name='delete'),
]
