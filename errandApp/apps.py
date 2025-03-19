from django.apps import AppConfig


class ErrandappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'errandApp'

    def ready(self):
        import errandApp.signals