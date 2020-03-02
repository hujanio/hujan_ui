from django.urls import path, include

from . import views

app_name = 'maas'
urlpatterns = [
    path('machines', views.machines, name='machines'),
    path('machines/<slug:system_id>/details/', views.machine_details, name='machine_details'),
]
