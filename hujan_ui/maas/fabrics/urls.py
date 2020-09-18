from django.urls import path, include
from . import views
app_name = 'fabrics'
urlpatterns = [
    path('', views.index,name='index'),
    path('add/', views.add,name='add'), 
    path('edit/<int:fabric_id>/', views.edit,name='edit'), 
]
