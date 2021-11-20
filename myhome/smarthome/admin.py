from django.contrib import admin
from .models import Device, SmartDevice


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'model',
        'producer',
        'type',
        'location',
        'date_of_register',
        'date_of_purchase',
    ]


@admin.register(SmartDevice)
class SmartDeviceAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'model',
        'producer',
        'type',
        'location',
        'smart_software',
        'network_status',
        'power_status',
        'ip_address',
        'date_of_register',
        'date_of_purchase',
    ]
