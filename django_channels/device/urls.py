from django.urls import path
from . import views
# from customer import views

urlpatterns= [
    path('device', views.device, name='device'),
    path('customer_add_device', views.customer_add_device, name='customer_add_device'),
    path('customer_list_device_by_customer', views.customer_list_device_by_customer, name='customer_list_device_by_customer'),
    path('customer_list_customer_by_device', views.customer_list_customer_by_device, name='customer_list_customer_by_device'),
    path('list_device', views.list_device, name='list_device'),
    path('edit_device/<str:pk>', views.edit_device, name='edit_device'),
    path('delete_device/<str:pk>', views.delete_device, name='delete_device'),


    # Admin Device
    path('admin_add_device', views.admin_add_device, name='admin_add_device'),
    path('admin_list_device/<str:pk>', views.admin_list_device, name='admin_list_device'),
    path('admin_edit_device/<str:pk>', views.admin_edit_device, name='admin_edit_device'),
    path('admin_delete_device/<str:pk>', views.admin_delete_device, name='admin_delete_device'),
    path('admin_list_device_by_customer/<str:pk>', views.admin_list_device_by_customer, name='admin_list_device_by_customer'),

    path('admin_list_customer', views.admin_list_customer, name='admin_list_customer'),
]

