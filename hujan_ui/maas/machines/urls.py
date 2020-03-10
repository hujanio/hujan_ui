from django.urls import path, include

from . import views

app_name = 'machines'
urlpatterns = [
    path('', views.index, name='index'),
    path('<slug:system_id>/details/', views.details, name='details'),
    path('add/', views.add, name='add'),
]
