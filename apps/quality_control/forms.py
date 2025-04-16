from django import forms
from django.utils.translation import gettext_lazy as _
from .models import QualityControlRecord
from apps.orders.models import Component, Order

class QualityControlRecordForm(forms.ModelForm):
    """
    Form for creating and updating quality control records
    """
    class Meta:
        model = QualityControlRecord
        fields = ['component', 'status', 'comments']
        widgets = {
            'comments': forms.Textarea(attrs={'class': 'textarea', 'rows': 3, 'placeholder': 'Enter quality control comments'}),
        }
    
    def __init__(self, *args, **kwargs):
        order = kwargs.pop('order', None)
        super().__init__(*args, **kwargs)
        
        # If order is provided, filter components by that order and in QC state
        if order:
            self.fields['component'].queryset = Component.objects.filter(
                order=order,
                status=Order.STATUS_QC
            )
        
        # Add appropriate form classes
        self.fields['component'].widget.attrs.update({'class': 'select'})
        self.fields['status'].widget.attrs.update({'class': 'select'})

class ComponentQCUpdateForm(forms.Form):
    """
    Form for updating QC status of a component
    """
    CHOICES = QualityControlRecord.STATUS_CHOICES
    
    status = forms.ChoiceField(
        choices=CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'radio'})
    )
    comments = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'textarea',
            'rows': 3,
            'placeholder': 'Enter quality control comments'
        }),
        required=False
    ) 