from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils.translation import gettext_lazy as _


class Role(models.Model):
    """Role model for defining permissions groups"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    
    # Linking to Django's built-in permissions system
    permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('permissions'),
        blank=True,
    )
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = _('role')
        verbose_name_plural = _('roles')


class Team(models.Model):
    """Team/Department model"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = _('team')
        verbose_name_plural = _('teams')


class User(AbstractUser):
    """Extended User model with additional fields"""
    # Link user to a team
    team = models.ForeignKey(
        Team,
        on_delete=models.SET_NULL,
        related_name='team_members',
        null=True,
        blank=True
    )
    
    # Link user to roles (many-to-many)
    roles = models.ManyToManyField(
        Role,
        related_name='role_users',
        blank=True
    )
    
    # Additional fields
    job_title = models.CharField(max_length=100, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    
    # Audit fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.get_full_name() or self.username
    
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        
    def is_admin(self):
        """Check if user has administrator role"""
        return self.is_superuser or self.roles.filter(name='Administrator').exists()
    
    def has_role(self, role_name):
        """Check if user has a specific role"""
        return self.roles.filter(name=role_name).exists()
