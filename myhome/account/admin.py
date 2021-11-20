from django.contrib import admin

from .models import UserProfile


@admin.register(UserProfile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'country',
        'country_code',
        'zip_code',
        'open_weather_map_appi_id',
    ]
