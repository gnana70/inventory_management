from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

from .models import Order, Component, OrderStatusHistory

User = get_user_model()

class OrderForm(forms.ModelForm):
    """
    Form for creating and updating orders
    """
    class Meta:
        model = Order
        fields = [
            'request_id', 'requested_amount', 'actual_amount',
            'requested_team', 'status', 'notes'
        ]
        widgets = {
            'request_id': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Request ID (optional)'}),
            'requested_amount': forms.NumberInput(attrs={'class': 'input', 'step': '0.01'}),
            'actual_amount': forms.NumberInput(attrs={'class': 'input', 'step': '0.01'}),
            'notes': forms.Textarea(attrs={'class': 'textarea', 'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['requested_team'].widget.attrs.update({'class': 'select'})
        self.fields['status'].widget.attrs.update({'class': 'select'})


class ComponentForm(forms.ModelForm):
    """
    Form for creating and updating components
    """
    class Meta:
        model = Component
        fields = [
            'id', 'name', 'value', 'package', 'part_number',
            'quantity', 'links', 'due_date', 'comments', 'status'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Component name'}),
            'value': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Value (e.g. 10K, 5V)'}),
            'package': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Package type'}),
            'part_number': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Part number'}),
            'quantity': forms.NumberInput(attrs={'class': 'input', 'min': 1}),
            'links': forms.Textarea(attrs={'class': 'textarea', 'rows': 2, 'placeholder': 'URLs or references'}),
            'due_date': forms.DateInput(attrs={'class': 'input', 'type': 'date'}),
            'comments': forms.Textarea(attrs={'class': 'textarea', 'rows': 2}),
            'status': forms.Select(attrs={'class': 'select'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make sure status has a default value
        if not self.instance.pk and 'status' not in self.initial:
            self.initial['status'] = Order.STATUS_REQUESTED


class OrderFilterForm(forms.Form):
    """
    Form for filtering orders in the list view
    """
    STATUS_CHOICES = [('', '--- All Statuses ---')] + list(Order.STATUS_CHOICES)
    
    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'select'})
    )
    requested_team = forms.ModelChoiceField(
        queryset=None,
        required=False,
        empty_label="--- All Teams ---",
        widget=forms.Select(attrs={'class': 'select'})
    )
    request_person = forms.ModelChoiceField(
        queryset=None,
        required=False,
        empty_label="--- All Requesters ---",
        widget=forms.Select(attrs={'class': 'select'})
    )
    date_from = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'input', 'type': 'date'})
    )
    date_to = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'input', 'type': 'date'})
    )
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'input', 'placeholder': 'Search orders...'}
        )
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from apps.accounts.models import Team
        
        # Get queryset for teams and requesters
        self.fields['requested_team'].queryset = Team.objects.all()
        self.fields['request_person'].queryset = User.objects.filter(
            is_active=True
        ).order_by('first_name', 'last_name')


class OrderStatusUpdateForm(forms.Form):
    """
    Form for updating order status
    """
    status = forms.ChoiceField(
        choices=Order.STATUS_CHOICES,
        widget=forms.Select(attrs={'class': 'select'})
    )
    notes = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={'class': 'textarea', 'rows': 3, 'placeholder': 'Status change notes (optional)'}
        )
    ) 