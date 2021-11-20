from datetime import date
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from yeelight import Bulb
from yeelight.main import _MODEL_SPECS, BulbException
from .forms import DeviceCreateForm, SmartDeviceCreateForm, YeelightBulbPowerForm, \
    YeelightBulbBrightForm, YeelightBulbCTForm
from .models import Device, SmartDevice


@login_required
def smart_home_dashboard(request):
    return render(request, 'smart_home_dashboard.html', {'section': 'smart_home'})


@login_required
def device_list(request):
    devices = Device.objects.all()
    return render(request, 'device/device_list.html', {'devices': devices, 'section': 'smart_home'})


@login_required
def device_detail(request, pk):
    device = get_object_or_404(Device, pk=pk)
    return render(request, 'device/device_detail.html', {'device': device, 'section': 'smart_home'})


@login_required
def device_create(request):
    if request.method == "POST":
        form = DeviceCreateForm(request.POST)
        if form.is_valid():
            device = form.save(commit=False)
            device.date_of_register = date.today()
            device.save()
            return redirect('device_detail', pk=device.pk)
    else:
        form = DeviceCreateForm()
    return render(request, 'device/device_create_form.html', {'form': form, 'section': 'smart_home'})


@login_required
def smart_device_list(request):
    smart_devices = SmartDevice.objects.all()
    return render(request, 'device/smart_device_list.html', {'smart_devices': smart_devices, 'section': 'smart_home'})


@login_required
def smart_device_detail(request, pk):
    smart_device = get_object_or_404(SmartDevice, pk=pk)
    if smart_device.smart_software == 'yeelight_bulb':
        # Creating a Bulb object based on the ip address from database
        yeelight_bulb = Bulb(smart_device.ip_address)
        #
        try:
            # Assigning the "model" attribute from device to a new variable. If device is offline,
            # get_capabilities() method returns None
            yeelight_bulb_model = yeelight_bulb.get_capabilities()['model']
            yeelight_bulb_properties = {key: value for key, value in yeelight_bulb.get_properties().items() if
                                        key in ['power', 'bright', 'ct', 'rgb']}
            context = {
                'smart_device': smart_device,
                'section': 'smart_home',
                'device_model': yeelight_bulb_model,
                'bulb_properties': yeelight_bulb_properties,
            }
            return render(request, 'device/smart_device_detail.html', context)
        # If device is offline get_capabilities()['model'] method returns TypeError
        except TypeError as te:
            if str(te) == "'NoneType' object is not subscriptable":
                context = {
                    'smart_device': smart_device,
                    'section': 'smart_home',
                    'device_model': "offline",
                }
                return render(request, 'device/smart_device_detail.html', context)

        """
        Here will be conditions of next smart software types
        """

    return render(
        request,
        'device/smart_device_detail.html',
        {'smart_device': smart_device, 'section': 'smart_home', 'device_model': None}
    )


@login_required
def smart_device_create(request):
    if request.method == "POST":
        form = SmartDeviceCreateForm(request.POST)
        if form.is_valid():
            smart_device = form.save(commit=False)
            smart_device.register = date.today()
            smart_device.save()
            return redirect('smart_device_detail', pk=smart_device.pk)
    else:
        form = SmartDeviceCreateForm()
    return render(request, 'device/smart_device_create_form.html', {'form': form, 'section': 'smart_home'})


@login_required
def smart_device_management(request, pk):
    smart_device = get_object_or_404(SmartDevice, pk=pk)
    if smart_device.smart_software == 'yeelight_bulb':
        yeelight_bulb = Bulb(smart_device.ip_address)
        try:
            yeelight_bulb_model = yeelight_bulb.get_capabilities()['model']
            yeelight_bulb_properties = {key: value for key, value in yeelight_bulb.get_properties().items() if
                                        key in ['power', 'bright', 'ct', 'rgb']}
            power_form = YeelightBulbPowerForm(initial={'power': yeelight_bulb_properties['power']})
            bright_form = YeelightBulbBrightForm(initial={'brightness': yeelight_bulb_properties['bright']})
            # Checking min and max value possibile to set of color temperature in Yeelight library
            bulb_ct_min_value = _MODEL_SPECS[yeelight_bulb_model]["color_temp"]["min"]
            bulb_ct_max_value = _MODEL_SPECS[yeelight_bulb_model]["color_temp"]["max"]

            if bulb_ct_min_value != bulb_ct_max_value:
                ct_form = YeelightBulbCTForm(
                    initial=({'color_temperature': yeelight_bulb_properties['ct']}),
                    ct_min_value=bulb_ct_min_value,
                    ct_max_value=bulb_ct_max_value,
                )
            # If bulb has constant color temperature value, ct_form variable has None value. In result of that user
            # will not see this form in smart_device_management template
            else:
                ct_form = None
            if request.method == 'POST':
                if 'power' in request.POST:
                    power_form = YeelightBulbPowerForm(request.POST)
                    if power_form.is_valid():
                        eval(f"yeelight_bulb.turn_{power_form.cleaned_data['power']}()")
                elif 'brightness' in request.POST:
                    bright_form = YeelightBulbBrightForm(request.POST)
                    if bright_form.is_valid():
                        yeelight_bulb.set_brightness(bright_form.cleaned_data['brightness'])
                elif 'color_temperature' in request.POST:
                    ct_form = YeelightBulbCTForm(
                        request.POST,
                        ct_min_value=bulb_ct_min_value,
                        ct_max_value=bulb_ct_max_value
                    )
                    if ct_form.is_valid():
                        yeelight_bulb.set_color_temp(ct_form.cleaned_data['color_temperature'])
            context = {
                'form1': power_form,
                'form2': bright_form,
                'form3': ct_form,
                'smart_device': smart_device,
                'section': 'smart_home',
                'device_model': yeelight_bulb_model,
                'bulb_properties': yeelight_bulb_properties,
            }
            return render(request, 'device/smart_device_management.html', context)
        except TypeError as te:
            if str(te) == "'NoneType' object is not subscriptable":
                context = {
                    'smart_device': smart_device,
                    'section': 'smart_home',
                    'error': 'offline',
                }
                return render(request, 'device/smart_device_detail.html', context)
        # This except part accounts a "socket error" which occurs occasionally
        # because of device's network connection problems
        except BulbException as be:
            if str(be) == "A socket error occurred when sending the command.":
                context = {
                    'smart_device': smart_device,
                    'section': 'smart_home',
                    'error': 'socket_error',
                }
                return render(request, 'device/smart_device_detail.html', context)
    return render(
        request,
        'device/smart_device_detail.html',
        {'smart_device': smart_device, 'section': 'smart_home', 'device_model': None}
    )
