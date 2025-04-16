from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.utils.translation import gettext_lazy as _

from .models import User, Team, Role


class CustomUserCreationForm(UserCreationForm):
    """Custom form for creating a new user"""
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'team', 'roles', 'job_title', 'phone_number')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make email required
        self.fields['email'].required = True


class CustomUserChangeForm(UserChangeForm):
    """Custom form for updating a user"""
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'team', 'roles', 'job_title', 'phone_number')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make email required
        self.fields['email'].required = True


class ProfileUpdateForm(forms.ModelForm):
    """Form for users to update their own profiles"""
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'job_title', 'phone_number')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make email required
        self.fields['email'].required = True


class TeamForm(forms.ModelForm):
    """Form for creating and updating teams"""
    class Meta:
        model = Team
        fields = ('name', 'description')


class RoleForm(forms.ModelForm):
    """Form for creating and updating roles"""
    class Meta:
        model = Role
        fields = ('name', 'description', 'permissions') 