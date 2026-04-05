# SkyPulse — Weather Application
### CS515 Unix Programming | IIIT Trichy | Assignment 03

A two-tier weather web application built with **Django** (backend) + **SQLite** (database) + a custom dark-theme frontend. Containerized with Docker and orchestrated with Kubernetes (Minikube).

## Features
- Real-time weather data from OpenWeatherMap API
- 5-day weather forecast
- Search history stored in SQLite database
- Favorite cities management
- Beautiful responsive dark UI

## Tech Stack
- **Backend**: Python 3.11, Django 4.2
- **Database**: SQLite
- **Frontend**: HTML5, CSS3, Vanilla JS
- **Containerization**: Docker (multi-stage build)
- **Orchestration**: Kubernetes (Minikube)
- **API**: OpenWeatherMap

## Quick Start
```bash
# 1. Get free API key from https://openweathermap.org/api
# 2. Run with Docker Compose
WEATHER_API_KEY=your_key docker-compose up
# 3. Visit http://localhost:8000
```

## Project Structure
```
weatherapp/
├── manage.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .gitignore
├── weatherproject/       # Django project settings
│   ├── settings.py
│   └── urls.py
├── weather/              # Main app
│   ├── models.py         # SearchHistory, FavoriteCity
│   ├── views.py          # Weather API logic
│   ├── urls.py
│   └── templates/weather/
│       ├── index.html
│       └── history.html
└── k8s/
    ├── deployment.yaml   # 2 replicas
    └── service.yaml      # NodePort :30080
```
