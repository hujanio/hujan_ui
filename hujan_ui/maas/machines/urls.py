from django.urls import path, include

from . import views

app_name = 'machines'
urlpatterns = [
    path('', views.index, name='index'),
    path('<slug:system_id>/details/', views.details, name='details'),
    path('add/', views.add, name='add'),
    path('load_machine/', views.load_machine, name='load_machine'),
    path('edit_physical/<str:system_id>/<int:id>/', views.edit_physical, name='edit_physical'),
    path('mark_disconnect/<str:system_id>/<int:id>/', views.mark_disconnect, name='mark_disconnect'),
    path('commission/<str:system_id>', views.machine_commission, name='machine_commission'),
    path('delete/<str:system_id>', views.delete_machine, name='delete_commission'),
    path('deploy/<str:system_id>', views.deploy_machine, name='deploy_machine'),
    path('onoff/<str:system_id>', views.onoff_machine, name='onoff_machine'),
]
