from django.urls import path, include
from . import views

app_name = 'subnets'


urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.add, name='add'),
    path('<int:subnet_id>/detail/', views.detail, name='subnet_detail'),
    path('<int:subnet_id>/edit/', views.edit, name='subnet_edit'),
    path('<int:subnet_id>/delete/', views.delete, name='subnet_delete'),
]
