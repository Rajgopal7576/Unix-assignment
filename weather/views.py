import requests
from django.shortcuts import render, redirect
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import SearchHistory, FavoriteCity
import json


def get_weather_data(city):
    """Fetch weather data from OpenWeatherMap API."""
    api_key = settings.WEATHER_API_KEY
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    
    params = {
        'q': city,
        'appid': api_key,
        'units': 'metric',
    }
    
    try:
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()
        return response.json(), None
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return None, "City not found. Please check the city name."
        elif response.status_code == 401:
            return None, "Invalid API key. Please configure a valid OpenWeatherMap API key."
        return None, f"API Error: {str(e)}"
    except requests.exceptions.ConnectionError:
        return None, "Connection error. Please check your internet connection."
    except requests.exceptions.Timeout:
        return None, "Request timed out. Please try again."
    except Exception as e:
        return None, f"Unexpected error: {str(e)}"


def get_forecast_data(city):
    """Fetch 5-day forecast from OpenWeatherMap API."""
    api_key = settings.WEATHER_API_KEY
    base_url = "https://api.openweathermap.org/data/2.5/forecast"
    
    params = {
        'q': city,
        'appid': api_key,
        'units': 'metric',
        'cnt': 40,
    }
    
    try:
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # Get one reading per day (noon reading)
        daily = {}
        for item in data['list']:
            date = item['dt_txt'].split(' ')[0]
            time = item['dt_txt'].split(' ')[1]
            if date not in daily or time == '12:00:00':
                daily[date] = {
                    'date': date,
                    'temp_max': item['main']['temp_max'],
                    'temp_min': item['main']['temp_min'],
                    'condition': item['weather'][0]['description'].title(),
                    'icon': item['weather'][0]['icon'],
                }
        
        return list(daily.values())[:5], None
    except Exception:
        return [], None


def index(request):
    """Main view - handles weather search."""
    weather_data = None
    forecast_data = []
    error = None
    city = ''
    
    if request.method == 'POST':
        city = request.POST.get('city', '').strip()
        
        if city:
            data, error = get_weather_data(city)
            
            if data and not error:
                weather_data = {
                    'city': data['name'],
                    'country': data['sys']['country'],
                    'temperature': round(data['main']['temp'], 1),
                    'feels_like': round(data['main']['feels_like'], 1),
                    'temp_max': round(data['main']['temp_max'], 1),
                    'temp_min': round(data['main']['temp_min'], 1),
                    'humidity': data['main']['humidity'],
                    'pressure': data['main']['pressure'],
                    'wind_speed': round(data['wind']['speed'] * 3.6, 1),  # m/s to km/h
                    'wind_deg': data['wind'].get('deg', 0),
                    'visibility': round(data.get('visibility', 0) / 1000, 1),
                    'condition': data['weather'][0]['description'].title(),
                    'icon': data['weather'][0]['icon'],
                    'main_condition': data['weather'][0]['main'],
                    'sunrise': data['sys']['sunrise'],
                    'sunset': data['sys']['sunset'],
                    'timezone': data['timezone'],
                    'clouds': data['clouds']['all'],
                    'lat': data['coord']['lat'],
                    'lon': data['coord']['lon'],
                }
                
                # Save to search history
                SearchHistory.objects.create(
                    city_name=weather_data['city'],
                    country_code=weather_data['country'],
                    temperature=weather_data['temperature'],
                    weather_condition=weather_data['condition'],
                    humidity=weather_data['humidity'],
                    wind_speed=weather_data['wind_speed'],
                )
                
                # Get forecast
                forecast_data, _ = get_forecast_data(city)
    
    # Get recent searches and favorites
    recent_searches = SearchHistory.objects.all()[:8]
    favorite_cities = FavoriteCity.objects.all()
    favorite_city_names = [f.city_name for f in favorite_cities]
    
    context = {
        'weather_data': weather_data,
        'forecast_data': forecast_data,
        'error': error,
        'city': city,
        'recent_searches': recent_searches,
        'favorite_cities': favorite_cities,
        'favorite_city_names': favorite_city_names,
    }
    
    return render(request, 'weatherfront/index.html', context)


@require_http_methods(["POST"])
def add_favorite(request):
    """Add a city to favorites."""
    data = json.loads(request.body)
    city = data.get('city', '').strip()
    
    if city:
        FavoriteCity.objects.get_or_create(city_name=city)
        return JsonResponse({'status': 'success', 'message': f'{city} added to favorites!'})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid city name'})


@require_http_methods(["POST"])
def remove_favorite(request):
    """Remove a city from favorites."""
    data = json.loads(request.body)
    city = data.get('city', '').strip()
    
    if city:
        FavoriteCity.objects.filter(city_name=city).delete()
        return JsonResponse({'status': 'success'})
    
    return JsonResponse({'status': 'error'})


def history(request):
    """View search history."""
    searches = SearchHistory.objects.all()[:50]
    return render(request, 'weatherfront/history.html', {'searches': searches})
