from django.apps import AppConfig
import gunicorn


class MedicalConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'medical'
                                                                                    