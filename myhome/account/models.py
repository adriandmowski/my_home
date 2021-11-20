from django.db import models
from django.conf import settings


class UserProfile(models.Model):
    COUNTRY_CHOICES = (
        ('us', 'USA'),
        ('india', 'India'),
        ('brazil', 'Brazil'),
        ('uk', 'United Kingdom'),
        ('russia', 'Russia'),
        ('turkey', 'Turkey'),
        ('france', 'Framce'),
        ('iran', 'Iran'),
        ('argentina', 'Argentina'),
        ('spain', 'Spain'),
        ('colombia', 'Colombia'),
        ('germany', 'Germany'),
        ('italy', 'Italy'),
        ('indonesia', 'Indonesia'),
        ('mexico', 'Mexico'),
        ('ukraine', 'Ukraine'),
        ('poland', 'Poland'),
        ('south-africa', 'South Africa'),
        ('philippines', 'Philippines'),
        ('malaysia', 'Malaysia'),
        ('netherlands', 'Netherlands'),
        ('peru', 'Peru'),
        ('iraq', 'Iraq'),
        ('thailand', 'Thailand'),
        ('czechia', 'Czechia'),
    )
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    country = models.CharField(max_length=100, choices=sorted(COUNTRY_CHOICES))
    country_code = models.CharField(max_length=2)
    zip_code = models.CharField(max_length=10)
    open_weather_map_appi_id = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.country}, {self.country_code}, {self.user}'
