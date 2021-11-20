from django import forms
from .models import Device, SmartDevice
from django.utils.translation import gettext_lazy as _
from datetime import date


class DeviceCreateForm(forms.ModelForm):
    class Meta:
        model = Device
        fields = ('name', 'model', 'producer', 'type', 'location', 'date_of_purchase')
        labels = {
            'name': _('Name'),
            'producer': _('Producer'),
            'type': _('Type'),
            'location': _('Location'),
            'date_of_purchase': _('Date of purchase'),
        }
        help_texts = {
            'date_of_purchase': _(f'date format: {date.today()}')
        }


class SmartDeviceCreateForm(forms.ModelForm):
    class Meta:
        model = SmartDevice
        fields = ('name', 'model', 'producer', 'type', 'smart_software', 'ip_address', 'location', 'date_of_purchase')
        labels = {
            'name': _('Name'),
            'producer': _('Producer'),
            'type': _('Type'),
            'smart_software': _('Smart device software'),
            'location': _('Location'),
            'date_of_purchase': _('Date of purchase'),
            'ip_address': _('IP address'),
        }
        help_texts = {
            'date_of_purchase': _(f'date format: {date.today()}')
        }


class YeelightBulbPowerForm(forms.Form):
    POWER_STATUS_CHOICES = (
        ('on', 'ON'),
        ('off', 'OFF'),
    )
    power = forms.ChoiceField(choices=POWER_STATUS_CHOICES)


class YeelightBulbBrightForm(forms.Form):
    brightness = forms.IntegerField(min_value=1, max_value=100)


class YeelightBulbCTForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.ct_min_value = kwargs.pop('ct_min_value')
        self.ct_max_value = kwargs.pop('ct_max_value')
        super(YeelightBulbCTForm, self).__init__(*args, **kwargs)
        self.fields['color_temperature'] = forms.IntegerField(min_value=self.ct_min_value, max_value=self.ct_max_value)



