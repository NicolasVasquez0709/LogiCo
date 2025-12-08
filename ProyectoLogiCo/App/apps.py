from django.apps import AppConfig
import django
django.setup()


class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'App'
