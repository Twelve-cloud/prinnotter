from django.apps import AppConfig


class JWT_AuthConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'jwt_auth'
    label = 'jwt_auth'
    verbose_name = 'JWT_Auth'
