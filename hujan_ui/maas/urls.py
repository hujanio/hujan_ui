from django.urls import path, include

from . import views

app_name = 'maas'
urlpatterns = [
    path('machines/', include('hujan_ui.maas.machines.urls')),
]
