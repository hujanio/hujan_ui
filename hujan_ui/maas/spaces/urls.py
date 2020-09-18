from django.urls import path
from . import views
app_name = 'spaces'

urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.index, name='add'),
    path('<int:space_id>/edit/', views.index, name='edit'),
    path('<int:space_id/delete/', views.index, name='delete'),
    path('<int:space_id/detail/', views.index, name='detail'),
]
