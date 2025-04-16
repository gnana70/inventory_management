from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class QualityControlConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.quality_control'
    verbose_name = _('Quality Control')
