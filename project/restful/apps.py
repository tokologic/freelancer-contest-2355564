from django.apps import AppConfig


class RestfulConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "project.restful"

    def ready(self):
        import project.restful.schema_extensions  # noqa
