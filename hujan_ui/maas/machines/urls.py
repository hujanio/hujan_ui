from django.urls import path, include

from . import views

app_name = 'machines'
urlpatterns = [
    path('', views.index, name='index'),
    path('<slug:system_id>/details/', views.details, name='details'),
    path('add/', views.add, name='add'),
    path('load_machine/', views.load_machine, name='load_machine'),
    path('edit_physical/<str:system_id>/<int:id>/', views.edit_physical, name='edit_physical'),
]
