from django.db import models
from django.utils import timezone
import socket
import re
from . import smart_functions


class Device(models.Model):
    name = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    producer = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    date_of_register = models.DateField(default=timezone.now)
    date_of_purchase = models.DateField(blank=True, null=True)

    class Meta:
        ordering = ('name', )

    def __str__(self):
        return self.name


class SmartDevice(Device):
    SMART_SOFTWARE_CHOICES = smart_functions.smart_software_tuples
    NETWORK_STATUS_CHOICES = (
        ('online', 'on-line'),
        ('offline', 'off-line'),
    )
    POWER_STATUS_CHOICES = (
        ('on', 'ON'),
        ('off', 'OFF'),
    )
    smart_software = models.CharField(
        max_length=50,
        choices=SMART_SOFTWARE_CHOICES,
        default=None,
        blank=True
    )
    network_status = models.CharField(
        max_length=10,
        choices=NETWORK_STATUS_CHOICES,
        default='offline'
    )
    power_status = models.CharField(
        max_length=10,
        choices=POWER_STATUS_CHOICES,
        default='off'
    )
    ip_address = models.CharField(
        max_length=15,
        default=re.match(r'(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.', socket.gethostbyname(socket.gethostname()))[0]
    )

    class Meta:
        ordering = ('name', )

    def __str__(self):
        return self.name


