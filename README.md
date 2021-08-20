# Dashboard

## About The Project
Dashboard for plotting functions using admin panel

## Built With
- **Django** for backend
- **Celery** as a task execution backend
- **Postgres** 
- **RabbitMQ** as a broker for Celery
- **Redis** as a backend for results for Celery
- **Highcharts** for rendering charts

## How to run

1. clone this repo
2. run `docker-compose up -d`
3. To create admin user: `docker exec -it <container_id> python manage.py createsuperuser`

## How to improve

1. Add nginx to serve static and media instead of django
2. Remove DEBUG=True from settings after setting up static server
3. Better error handling
