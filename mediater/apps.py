from django.apps import AppConfig


class MediaterConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mediater'

    def ready(self) -> None:
        import mediater.signals.handlers
