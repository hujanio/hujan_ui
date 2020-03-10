from django.urls import path, include

from . import views

app_name = 'dns'
urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.add, name='add'),
]
