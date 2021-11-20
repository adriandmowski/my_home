# My_home 

## Introduction
#### The project has been created in order to consolidate knowledge gained during the courses and to optimize a way of managing home devices.

## Technologies
### Python 3.8
### Django 3.2
### Libraries:
#### yeelight 0.7

## Start-up

#### It is recommended to create a profile in Django administration panel after creating an user account. This will allow to display information about new COVID-19 cases and a current temperature in the main bar.

#### Displaying the number of new COVID-19 cases in the main bar: enter a country name in your profile. Currently the application supports 20 countries.

#### Display the current temperature in °C: enter a country name, country code in „ISO 3166-1 alfa-2” standard and Openweathermaps’s api key. In order to generate your own api key, please register at https://home.openweathermap.org/. After registration, please generate the key in user/”My API keys” tab.

## Project status

#### The application allows to add devices in database. Devices which are connected to a home network can be saved as „Smart Devices”. It allows to control these devices via the app. Currently the application allows to control (turn on/off, set brightness, set color temperature) Yeelight bulbs using the „yeelight 0.7” library. Support for more devices will be added in the future.
