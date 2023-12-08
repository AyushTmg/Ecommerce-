from django.apps import AppConfig


class PrimaryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'primary'

    def ready(self) -> None:
        import primary.signals.handlers
