from datetime import datetime, date
from django import template
import re
import requests
from account.models import UserProfile

register = template.Library()


@register.inclusion_tag('news/coronavirus.html')
def coronavirus_today(user_id):
    try:
        profile = UserProfile.objects.get(user_id=user_id)
        my_country = profile.country
        date_today = str(datetime.today().strftime('%B')) + ' ' + str(datetime.today().day)
        coronameter_page = requests.get(f'https://www.worldometers.info/coronavirus/country/{my_country}/')
        pattern = f'{date_today} ' + r'\(GMT\)</h4></div><div id="newsdate' + f'{date.today()}' + \
                    r'"><span id="updates" class="news_category_title">Updates</span><div class="news_post">\n' \
                    r'<div class="news_body">\n<ul class="news_ul"><li class="news_li"><strong>(\d{1,3}(,\d{1,3})*)'
        coronavirus_object = re.search(pattern, coronameter_page.text)
        try:
            coronavirus_cases_today = coronavirus_object.group(1)
            cases_today = int(coronavirus_cases_today.replace(',', ''))
            return {'profile': profile, 'cases_today': cases_today, 'my_country': my_country.capitalize()}
        except AttributeError:
            cases_today = None
            return {'profile': profile, 'cases_today': cases_today, 'my_country': my_country.capitalize()}
    except UserProfile.DoesNotExist:
        return {'profile': None, 'cases_today': None, 'my_country': None}


@register.inclusion_tag('news/temperature.html')
def temperature_now(user_id):
    try:
        profile = UserProfile.objects.get(user_id=user_id)
        zip_code = profile.zip_code
        country_code = profile.country_code
        appid = profile.open_weather_map_appi_id
        weather_api_call = requests.get(
            f'http://api.openweathermap.org/data/2.5/weather?zip={zip_code},{country_code}&appid={appid}'
        )
        celsius_temperature = round(weather_api_call.json()['main']['temp'] - 273.15, 1)
        return {'profile': profile, 'temperature': celsius_temperature}
    except UserProfile.DoesNotExist:
        return {'profile': None, 'temperature': None}