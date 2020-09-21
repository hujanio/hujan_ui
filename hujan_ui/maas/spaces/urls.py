from django.urls import path
from . import views
app_name = 'spaces'

urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.add, name='add'),
    path('<int:space_id>/edit/', views.edit, name='edit'),
    path('<int:space_id>/delete/', views.delete, name='delete'),
    path('<int:space_id>/detail/', views.detail, name='detail')
]
