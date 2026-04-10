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

### Using Docker Compose (Recommended for Local Dev)
```bash
# 1. Run in detached mode and build the container
docker-compose up -d --build
# 2. Visit http://localhost:8000
```

### Using Kubernetes (Minikube)
```bash
# 1. Start Minikube & use its Docker daemon
minikube start
eval $(minikube docker-env)

# 2. Build the image locally
docker build -t skypulse:latest .

# 3. Apply the deployment and service manifests
kubectl apply -f k8s/

# 4. Access the application
minikube service skypulse-service --url
```

## Changing the API Key
A default OpenWeatherMap API key is currently bundled with the project for convenience. To update it with your own key, modify the `WEATHER_API_KEY` variable in the following two files:
- `docker-compose.yml`
- `k8s/deployment.yaml`

## Project Structure
```
weatherweb/
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
│   └── templates/weatherfront/
│       ├── index.html
│       └── history.html
└── k8s/
    ├── deployment.yaml   # 2 replicas
    └── service.yaml      # NodePort :30080
```
