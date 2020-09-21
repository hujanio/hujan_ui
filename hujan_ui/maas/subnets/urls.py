from django.urls import path, include
from . import views

app_name = 'subnets'
urlpatterns = [
    path('',views.index,name='index'),
    path('add/',views.add,name='add'),
    path('<int:fabric_id>/fabric/',views.fabric_detail,name='fabric_detail'),
    path('<int:vlan_id>/vlan/',views.vlan_detail,name='vlan_detail'),
    path('<int:subnet_id>/subnet/',views.detail,name='subnet_detail'),
    path('<int:subnet_id>/edit/',views.edit,name='subnet_edit'),
    path('<int:subnet_id>/delete/',views.delete,name='subnet_delete'),
]
