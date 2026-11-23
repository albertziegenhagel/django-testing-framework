from django.apps import AppConfig


class DtfConfig(AppConfig):
    name = 'dtf'
    verbose_name = 'Django Testing Framework'

    default_auto_field = 'django.db.models.AutoField'

    def ready(self):
        from .webhooks import connect_webhook_signals
        import dtf.signals
        connect_webhook_signals()
