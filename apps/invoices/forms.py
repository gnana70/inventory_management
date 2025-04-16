from django import forms
from django.utils.translation import gettext_lazy as _
from django.forms.models import inlineformset_factory, BaseInlineFormSet

from .models import Invoice, InvoiceComponent, InvoiceAttachment
from apps.orders.models import Order, Component

class InvoiceForm(forms.ModelForm):
    """
    Form for creating and editing invoices.
    """
    class Meta:
        model = Invoice
        fields = ['invoice_number', 'invoice_date', 'company_name', 'notes']
        widgets = {
            'invoice_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }


class InvoiceComponentForm(forms.ModelForm):
    """
    Form for adding components to an invoice.
    """
    class Meta:
        model = InvoiceComponent
        fields = [
            'component', 'name', 'value', 'package', 'part_number',
            'quantity', 'price_per_unit', 'gst_percentage', 'warranty_information'
        ]
        widgets = {
            'component': forms.Select(attrs={'class': 'form-select component-select'}),
            'warranty_information': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        order = kwargs.pop('order', None)
        super().__init__(*args, **kwargs)
        
        # If an order is specified, limit component choices to that order
        if order:
            self.fields['component'].queryset = Component.objects.filter(order=order)
        
        # Add 'readonly' attribute to the fields that get populated from the component
        for field_name in ['name', 'value', 'package', 'part_number']:
            self.fields[field_name].widget.attrs.update({
                'readonly': 'readonly',
                'class': 'form-control'
            })
        
        # Add appropriate classes to number fields
        for field_name in ['quantity', 'price_per_unit', 'gst_percentage']:
            self.fields[field_name].widget.attrs.update({
                'class': 'form-control'
            })


class BaseInvoiceComponentFormSet(BaseInlineFormSet):
    """
    Base formset for invoice components with validation.
    """
    def clean(self):
        """Validate that at least one component is added."""
        super().clean()
        if any(self.errors):
            return
        
        if not any(form.cleaned_data and not form.cleaned_data.get('DELETE', False)
                   for form in self.forms):
            raise forms.ValidationError(_("At least one component must be added to the invoice."))


class InvoiceAttachmentForm(forms.ModelForm):
    """
    Form for adding attachments to an invoice.
    """
    class Meta:
        model = InvoiceAttachment
        fields = ['file', 'description']
        widgets = {
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'file': forms.FileInput(attrs={'class': 'form-control'})
        }


# Create formsets
InvoiceComponentFormSet = inlineformset_factory(
    Invoice, 
    InvoiceComponent,
    form=InvoiceComponentForm,
    formset=BaseInvoiceComponentFormSet,
    extra=1,
    can_delete=True
)

InvoiceAttachmentFormSet = inlineformset_factory(
    Invoice,
    InvoiceAttachment,
    form=InvoiceAttachmentForm,
    extra=1,
    can_delete=True
)


class OrderInvoiceForm(forms.Form):
    """
    Form for selecting an order to invoice.
    """
    order = forms.ModelChoiceField(
        queryset=Order.objects.all(),
        label=_("Order"),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    invoice_all_components = forms.BooleanField(
        label=_("Create single invoice for all components"),
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )


class BulkInvoiceForm(forms.Form):
    """
    Form for creating a single invoice for multiple components.
    """
    invoice_number = forms.CharField(
        label=_("Invoice Number"),
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    invoice_date = forms.DateField(
        label=_("Invoice Date"),
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    company_name = forms.CharField(
        label=_("Company/Vendor Name"),
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    components = forms.ModelMultipleChoiceField(
        queryset=Component.objects.all(),
        label=_("Components"),
        widget=forms.SelectMultiple(attrs={'class': 'form-select'})
    )
    price_per_unit = forms.DecimalField(
        label=_("Price Per Unit"),
        min_value=0,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    gst_percentage = forms.DecimalField(
        label=_("GST Percentage"),
        min_value=0,
        decimal_places=2,
        initial=18.00,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    warranty_information = forms.CharField(
        label=_("Warranty Information"),
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    notes = forms.CharField(
        label=_("Notes"),
        required=False,
        widget=forms.Textarea(attrs={'rows': 3, 'class': 'form-control'})
    )
    
    def __init__(self, *args, **kwargs):
        order = kwargs.pop('order', None)
        super().__init__(*args, **kwargs)
        
        # If an order is specified, limit component choices to that order
        if order:
            self.fields['components'].queryset = Component.objects.filter(order=order) 