from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

from .models import User, Role


@receiver(post_save, sender=User)
def assign_default_role(sender, instance, created, **kwargs):
    """Assign a default role to newly created users"""
    if created:
        # Only assign default role if the user doesn't have any roles yet
        if not instance.roles.exists():
            # Get or create 'Basic User' role
            basic_role, created = Role.objects.get_or_create(
                name='Basic User',
                defaults={'description': 'Default role with basic permissions'}
            )
            
            # Assign role to user
            instance.roles.add(basic_role) 