from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import get_user_model

from .models import User, Team, Role
from .forms import (
    CustomUserCreationForm, CustomUserChangeForm, ProfileUpdateForm,
    TeamForm, RoleForm
)

# Create your views here.

# User Profile Views
@login_required
def profile_view(request):
    """Display user profile"""
    return render(request, 'accounts/profile.html', {'user': request.user})

@login_required
def profile_edit(request):
    """Edit user profile"""
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('accounts:profile')
    else:
        form = ProfileUpdateForm(instance=request.user)
    
    return render(request, 'accounts/profile_edit.html', {'form': form})

# User Management Views
@login_required
def user_list(request):
    """List all users"""
    users = User.objects.all().order_by('username')
    return render(request, 'accounts/user_list.html', {'users': users})

@login_required
def user_create(request):
    """Create a new user"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'User created successfully.')
            return redirect('accounts:user_list')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'accounts/user_form.html', {'form': form, 'title': 'Create User'})

@login_required
def user_detail(request, user_id):
    """Display user details"""
    user = get_object_or_404(User, id=user_id)
    return render(request, 'accounts/user_detail.html', {'user': user})

@login_required
def user_edit(request, user_id):
    """Edit an existing user"""
    user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'User updated successfully.')
            return redirect('accounts:user_detail', user_id=user.id)
    else:
        form = CustomUserChangeForm(instance=user)
    
    return render(request, 'accounts/user_form.html', {'form': form, 'title': 'Edit User', 'user': user})

# Team Management Views
@login_required
def team_list(request):
    """List all teams"""
    teams = Team.objects.all().order_by('name')
    return render(request, 'accounts/team_list.html', {'teams': teams})

@login_required
def team_create(request):
    """Create a new team"""
    if request.method == 'POST':
        form = TeamForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Team created successfully.')
            return redirect('accounts:team_list')
    else:
        form = TeamForm()
    
    return render(request, 'accounts/team_form.html', {'form': form, 'title': 'Create Team'})

@login_required
def team_detail(request, team_id):
    """Display team details"""
    team = get_object_or_404(Team, id=team_id)
    team_members = User.objects.filter(team=team)
    return render(request, 'accounts/team_detail.html', {'team': team, 'team_members': team_members})

@login_required
def team_edit(request, team_id):
    """Edit an existing team"""
    team = get_object_or_404(Team, id=team_id)
    
    if request.method == 'POST':
        form = TeamForm(request.POST, instance=team)
        if form.is_valid():
            form.save()
            messages.success(request, 'Team updated successfully.')
            return redirect('accounts:team_detail', team_id=team.id)
    else:
        form = TeamForm(instance=team)
    
    return render(request, 'accounts/team_form.html', {'form': form, 'title': 'Edit Team', 'team': team})

# Role Management Views
@login_required
def role_list(request):
    """List all roles"""
    roles = Role.objects.all().order_by('name')
    return render(request, 'accounts/role_list.html', {'roles': roles})

@login_required
def role_create(request):
    """Create a new role"""
    if request.method == 'POST':
        form = RoleForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Role created successfully.')
            return redirect('accounts:role_list')
    else:
        form = RoleForm()
    
    return render(request, 'accounts/role_form.html', {'form': form, 'title': 'Create Role'})

@login_required
def role_detail(request, role_id):
    """Display role details"""
    role = get_object_or_404(Role, id=role_id)
    role_users = User.objects.filter(roles=role)
    return render(request, 'accounts/role_detail.html', {'role': role, 'role_users': role_users})

@login_required
def role_edit(request, role_id):
    """Edit an existing role"""
    role = get_object_or_404(Role, id=role_id)
    
    if request.method == 'POST':
        form = RoleForm(request.POST, instance=role)
        if form.is_valid():
            form.save()
            messages.success(request, 'Role updated successfully.')
            return redirect('accounts:role_detail', role_id=role.id)
    else:
        form = RoleForm(instance=role)
    
    return render(request, 'accounts/role_form.html', {'form': form, 'title': 'Edit Role', 'role': role})
