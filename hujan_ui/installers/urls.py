from django.urls import path, include

from . import views

app_name = 'website'
urlpatterns = [
    path('', views.index, name='index'),
    path('sales-order', views.sales_order, name='sales_order'),
    path('returns-order', views.returns_order, name='returns_order'),
    path('sales-report', views.reports, name='sales_report'),
    path('invoice', views.invoice, name='invoice'),
    path('signup', views.signup, name='signup')
]
