from flask import Flask, render_template, request
import requests
from datetime import datetime
from collections import defaultdict

app = Flask(__name__)

API_KEY = '7d12c60e3cc5308bc0022a60358914db'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/weather', methods=['POST'])
def weather():
    # Get the city, latitude, and longitude from the form
    city = request.form.get('city')
    latitude = request.form.get('latitude')
    longitude = request.form.get('longitude')

    # If latitude and longitude are provided, fetch weather data based on those
    if latitude and longitude:
        location = "Your Location"
        weather_data = get_weather_data_by_coordinates(latitude, longitude)
        forecast_data = get_forecast_data_by_coordinates(latitude, longitude)
    # If city is provided, fetch weather data based on the city
    elif city:
        location = city
        weather_data = get_weather_data(city)
        forecast_data = get_forecast_data(city)
    else:
        return render_template('index.html', error="No location or city provided.")

    if weather_data:
        return render_template('index.html', weather=weather_data, forecast=forecast_data, location=location)
    else:
        return render_template('index.html', error="Weather data could not be retrieved.")

def get_weather_data(city):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric'
    response = requests.get(url)
    data = response.json()

    if data['cod'] == 200:
        sunrise_time = datetime.utcfromtimestamp(data['sys']['sunrise']).strftime('%H:%M:%S')
        sunset_time = datetime.utcfromtimestamp(data['sys']['sunset']).strftime('%H:%M:%S')

        return {
            'temp': data['main']['temp'],
            'feels_like': data['main']['feels_like'],
            'temp_min': data['main']['temp_min'],
            'temp_max': data['main']['temp_max'],
            'humidity': data['main']['humidity'],
            'pressure': data['main']['pressure'],
            'wind_speed': data['wind']['speed'],
            'wind_deg': data['wind']['deg'],
            'description': data['weather'][0]['description'],
            'icon': data['weather'][0]['icon'],
            'visibility': data.get('visibility', 'N/A'),
            'cloudiness': data['clouds']['all'],
            'country': data['sys']['country'],
            'sunrise': sunrise_time,
            'sunset': sunset_time,
            'city': data['name']
        }
    else:
        return None

def get_weather_data_by_coordinates(lat, lon):
    url = f'http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric'
    response = requests.get(url)
    data = response.json()

    if data['cod'] == 200:
        sunrise_time = datetime.utcfromtimestamp(data['sys']['sunrise']).strftime('%H:%M:%S')
        sunset_time = datetime.utcfromtimestamp(data['sys']['sunset']).strftime('%H:%M:%S')

        return {
            'temp': data['main']['temp'],
            'feels_like': data['main']['feels_like'],
            'temp_min': data['main']['temp_min'],
            'temp_max': data['main']['temp_max'],
            'humidity': data['main']['humidity'],
            'pressure': data['main']['pressure'],
            'wind_speed': data['wind']['speed'],
            'wind_deg': data['wind']['deg'],
            'description': data['weather'][0]['description'],
            'icon': data['weather'][0]['icon'],
            'visibility': data.get('visibility', 'N/A'),
            'cloudiness': data['clouds']['all'],
            'country': data['sys']['country'],
            'sunrise': sunrise_time,
            'sunset': sunset_time,
            'city': data['name']
        }
    else:
        return None

def get_forecast_data(city):
    url = f'http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric'
    response = requests.get(url)
    data = response.json()

    if data['cod'] == '200':
        daily_forecast = defaultdict(list)

        # Organizes forecasts by day
        for forecast in data['list']:
            date = datetime.utcfromtimestamp(forecast['dt']).strftime('%Y-%m-%d')
            daily_forecast[date].append({
                'temp': forecast['main']['temp'],
                'description': forecast['weather'][0]['description'],
                'icon': forecast['weather'][0]['icon']
            })

        # Summarize data by taking avg temp per day
        summarized_forecast = []
        for date, day_data in daily_forecast.items():
            avg_temp = sum(item['temp'] for item in day_data) / len(day_data)
            description = day_data[0]['description']
            icon = day_data[0]['icon']
            summarized_forecast.append({
                'date': date,
                'avg_temp': round(avg_temp, 1),
                'description': description,
                'icon': icon
            })

        return summarized_forecast
    else:
        return None

def get_forecast_data_by_coordinates(lat, lon):
    url = f'http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY}&units=metric'
    response = requests.get(url)
    data = response.json()

    if data['cod'] == '200':
        daily_forecast = defaultdict(list)

        # Organizes forecasts by day
        for forecast in data['list']:
            date = datetime.utcfromtimestamp(forecast['dt']).strftime('%Y-%m-%d')
            daily_forecast[date].append({
                'temp': forecast['main']['temp'],
                'description': forecast['weather'][0]['description'],
                'icon': forecast['weather'][0]['icon']
            })

        # Summarize data by taking avg temp per day
        summarized_forecast = []
        for date, day_data in daily_forecast.items():
            avg_temp = sum(item['temp'] for item in day_data) / len(day_data)
            description = day_data[0]['description']
            icon = day_data[0]['icon']
            summarized_forecast.append({
                'date': date,
                'avg_temp': round(avg_temp, 1),
                'description': description,
                'icon': icon
            })

        return summarized_forecast
    else:
        return None

if __name__ == '__main__':
    app.run(debug=True)
