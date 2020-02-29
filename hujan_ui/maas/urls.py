from django.urls import path, include

from . import views

app_name = 'maas'
urlpatterns = [
    path('machines', views.machines, name='machines'),
]
