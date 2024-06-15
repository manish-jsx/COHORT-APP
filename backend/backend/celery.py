# backend/celery.py
import os

from celery import Celery
from django.conf import settings

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

app = Celery('backend')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means allcelery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

# Optional: Add task configuration if needed
app.conf.update(
    task_serializer='json',  # Default task serializer
    result_serializer='json', # Default result serializer
    accept_content=['json'],  # List of accepted content types
    timezone='UTC',  # Set your desired timezone
    enable_utc=True,   # Enable UTC timezones
    # Other Celery configuration options
)
