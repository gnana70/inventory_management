from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.accounts'
    verbose_name = _('Accounts & Users')
    
    def ready(self):
        """Import signal handlers when app is ready"""
        import apps.accounts.signals
