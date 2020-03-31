from django.urls import path, include

from . import views

app_name = 'inventories'
urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.add, name='add'),
    path('edit/<int:id>', views.edit, name='edit'),
]
