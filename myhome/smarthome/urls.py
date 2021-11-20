from django.urls import path
from . import views

urlpatterns = [
    path('', views.smart_home_dashboard, name='smart_home'),
    path('devices/', views.device_list, name='devices'),
    path('device/<int:pk>/', views.device_detail, name='device_detail'),
    path('device/new', views.device_create, name='device_create'),
    path('smartdevices/', views.smart_device_list, name='smart_devices'),
    path('smartdevice/<int:pk>/', views.smart_device_management, name='smart_device_management'),
    path('smartdevice/new', views.smart_device_create, name='smart_device_create'),
    path('smartdevice/<int:pk>/detail', views.smart_device_detail, name='smart_device_detail'),
]
