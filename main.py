import requests
import json
from datetime import datetime
import os
import threading


FILE_DIR = os.path.dirname(os.path.abspath(__file__))

with open(FILE_DIR + '/cfg/main.cfg', 'r') as FileRead:
    FileJsonRead = json.load(FileRead)
    KEY = FileJsonRead['key']
    UNITS = FileJsonRead['units']
    PERIOD = 60 / FileJsonRead['period']


def write_to_log(text):
    with open(FILE_DIR + '/logs/main.log', 'a') as LogFile:
        LogFile.write(str(datetime.now()) + ' ' + text)


write_to_log('INFO: started')


def main():
    threading.Timer(interval=PERIOD, function=main).start()

    req_last_weather = requests.get("https://api.openweathermap.org/data/2.5/weather?lat=59.8944&lon=30.2642&appid=" + KEY + "&units=" + UNITS)
    req_forecast = requests.get("https://api.openweathermap.org/data/2.5/forecast?lat=59.8944&lon=30.2642&appid=" + KEY + "&units=" + UNITS + "&cnt=7")

    if (not req_last_weather) or (not req_forecast):
        print('QOTWS: something went wrong with API')
        exit()

    resp_last_weather = json.loads(req_last_weather.text)
    resp_forecast = json.loads(req_forecast.text)

    try:
        with open(FILE_DIR + '/weather/last_weather.json', 'r') as LastWeatherFile:
            LastWeatherFileJson = json.load(LastWeatherFile)

        LastWeatherFileJson['temp'] = resp_last_weather['main']['temp']
        LastWeatherFileJson['temp_feels'] = resp_last_weather['main']['feels_like']
        LastWeatherFileJson['temp_min'] = resp_last_weather['main']['temp_min']
        LastWeatherFileJson['temp_max'] = resp_last_weather['main']['temp_max']
        LastWeatherFileJson['pressure'] = resp_last_weather['main']['pressure']
        LastWeatherFileJson['humidity'] = resp_last_weather['main']['humidity']
        LastWeatherFileJson['visibility'] = resp_last_weather['visibility']
        LastWeatherFileJson['wind_speed'] = resp_last_weather['wind']['speed']
        LastWeatherFileJson['wind_deg'] = resp_last_weather['wind']['deg']
        LastWeatherFileJson['weather'] = resp_last_weather['weather'][0]['icon']
        LastWeatherFileJson['clouds_percentage'] = resp_last_weather['clouds']['all']
        LastWeatherFileJson['sunrise'] = datetime.utcfromtimestamp(resp_last_weather['sys']['sunrise']).strftime('%H:%M:%S')
        LastWeatherFileJson['sunset'] = datetime.utcfromtimestamp(resp_last_weather['sys']['sunset']).strftime('%H:%M:%S')

        with open(FILE_DIR + '/weather/last_weather.json', 'w') as LastWeatherFile:
            LastWeatherFile.write(json.dumps(LastWeatherFileJson))
    except:
        write_to_log('ERROR: something went wrong with last weather JSON of API')
        print('QOTWS: something went wrong with last weather JSON of API')
        exit()

    try:
        with open(FILE_DIR + '/weather/forecast.json', 'r') as ForecastFile:
            ForecastFileJson = json.load(ForecastFile)

        for i in range(7):
            ForecastFileJson[i]['temp'] = resp_forecast['list'][i]['main']['temp']
            ForecastFileJson[i]['temp_feels'] = resp_forecast['list'][i]['main']['feels_like']
            ForecastFileJson[i]['temp_min'] = resp_forecast['list'][i]['main']['temp_min']
            ForecastFileJson[i]['temp_max'] = resp_forecast['list'][i]['main']['temp_max']
            ForecastFileJson[i]['pressure'] = resp_forecast['list'][i]['main']['pressure']
            ForecastFileJson[i]['humidity'] = resp_forecast['list'][i]['main']['humidity']
            ForecastFileJson[i]['visibility'] = resp_forecast['list'][i]['visibility']
            ForecastFileJson[i]['wind_speed'] = resp_forecast['list'][i]['wind']['speed']
            ForecastFileJson[i]['wind_deg'] = resp_forecast['list'][i]['wind']['deg']
            ForecastFileJson[i]['weather'] = resp_forecast['list'][i]['weather'][0]['icon']
            ForecastFileJson[i]['clouds_percentage'] = resp_forecast['list'][i]['clouds']['all']

        with open(FILE_DIR + '/weather/forecast.json', 'w') as ForecastFile:
            ForecastFile.write(json.dumps(ForecastFileJson))
    except:
        write_to_log('ERROR: something went wrong with forecast JSON of API')
        print('QOTWS: something went wrong with forecast JSON of API')
        exit()


threading.Timer(interval=PERIOD, function=main).start()