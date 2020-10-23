from django.urls import path, include

from . import views

app_name = 'servers'
urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.add, name='add'),
    path('edit/<int:id>', views.edit, name='edit'),
    path('delete/<int:id>', views.delete, name='delete'),
    path('reset/', views.reset, name='reset'),
]
