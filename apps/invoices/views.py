from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.utils import timezone
from django.urls import reverse
from django.http import HttpResponseRedirect

from .models import Invoice, InvoiceComponent, InvoiceAttachment
from .forms import (
    InvoiceForm, InvoiceComponentFormSet, InvoiceAttachmentFormSet,
    OrderInvoiceForm, BulkInvoiceForm
)
from apps.orders.models import Order, Component

@login_required
def invoice_list(request):
    """
    Display a list of all invoices.
    """
    invoices = Invoice.objects.all().select_related('created_by')
    
    context = {
        'invoices': invoices,
        'title': 'Invoices'
    }
    return render(request, 'invoices/invoice_list.html', context)

@login_required
def invoice_detail(request, invoice_id):
    """
    Display the details of a specific invoice.
    """
    invoice = get_object_or_404(Invoice.objects.select_related('created_by'), pk=invoice_id)
    invoice_components = invoice.invoice_components.all().select_related('component')
    invoice_attachments = invoice.attachments.all().select_related('uploaded_by')
    
    context = {
        'invoice': invoice,
        'invoice_components': invoice_components,
        'invoice_attachments': invoice_attachments,
        'title': f'Invoice {invoice.invoice_number}'
    }
    return render(request, 'invoices/invoice_detail.html', context)

@login_required
@transaction.atomic
def invoice_create(request):
    """
    Create a new invoice with components and attachments.
    """
    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        component_formset = InvoiceComponentFormSet(request.POST, prefix='components')
        attachment_formset = InvoiceAttachmentFormSet(request.POST, request.FILES, prefix='attachments')
        
        if form.is_valid() and component_formset.is_valid() and attachment_formset.is_valid():
            # Save invoice
            invoice = form.save(commit=False)
            invoice.created_by = request.user
            invoice.save()
            
            # Save invoice components
            component_instances = component_formset.save(commit=False)
            for component in component_instances:
                component.invoice = invoice
                component.save()
            
            # Save invoice attachments
            attachment_instances = attachment_formset.save(commit=False)
            for attachment in attachment_instances:
                attachment.invoice = invoice
                attachment.uploaded_by = request.user
                attachment.save()
            
            messages.success(request, f"Invoice {invoice.invoice_number} has been created successfully.")
            return redirect('invoices:detail', invoice_id=invoice.id)
    else:
        form = InvoiceForm()
        component_formset = InvoiceComponentFormSet(prefix='components')
        attachment_formset = InvoiceAttachmentFormSet(prefix='attachments')
    
    context = {
        'form': form,
        'component_formset': component_formset,
        'attachment_formset': attachment_formset,
        'title': 'Create Invoice'
    }
    return render(request, 'invoices/invoice_form.html', context)

@login_required
@transaction.atomic
def invoice_update(request, invoice_id):
    """
    Update an existing invoice.
    """
    invoice = get_object_or_404(Invoice, pk=invoice_id)
    
    if request.method == 'POST':
        form = InvoiceForm(request.POST, instance=invoice)
        component_formset = InvoiceComponentFormSet(
            request.POST, 
            prefix='components', 
            instance=invoice
        )
        attachment_formset = InvoiceAttachmentFormSet(
            request.POST, 
            request.FILES, 
            prefix='attachments', 
            instance=invoice
        )
        
        if form.is_valid() and component_formset.is_valid() and attachment_formset.is_valid():
            # Save invoice
            form.save()
            
            # Save invoice components
            component_formset.save()
            
            # Save invoice attachments
            attachment_instances = attachment_formset.save(commit=False)
            for attachment in attachment_instances:
                if not attachment.uploaded_by:
                    attachment.uploaded_by = request.user
                attachment.save()
            
            messages.success(request, f"Invoice {invoice.invoice_number} has been updated successfully.")
            return redirect('invoices:detail', invoice_id=invoice.id)
    else:
        form = InvoiceForm(instance=invoice)
        component_formset = InvoiceComponentFormSet(prefix='components', instance=invoice)
        attachment_formset = InvoiceAttachmentFormSet(prefix='attachments', instance=invoice)
    
    context = {
        'form': form,
        'component_formset': component_formset,
        'attachment_formset': attachment_formset,
        'invoice': invoice,
        'title': f'Update Invoice {invoice.invoice_number}'
    }
    return render(request, 'invoices/invoice_form.html', context)

@login_required
def select_order_for_invoice(request):
    """
    Select an order to create an invoice for.
    """
    if request.method == 'POST':
        form = OrderInvoiceForm(request.POST)
        if form.is_valid():
            order_id = form.cleaned_data['order'].id
            invoice_all = form.cleaned_data['invoice_all_components']
            
            if invoice_all:
                # Redirect to bulk invoice creation for the whole order
                return redirect('invoices:create_bulk_invoice', order_id=order_id)
            else:
                # Redirect to component selection for the order
                return redirect('invoices:select_components', order_id=order_id)
    else:
        form = OrderInvoiceForm()
    
    context = {
        'form': form,
        'title': 'Select Order for Invoice'
    }
    return render(request, 'invoices/select_order.html', context)

@login_required
@transaction.atomic
def create_bulk_invoice(request, order_id):
    """
    Create a single invoice for all components in an order.
    """
    order = get_object_or_404(Order, pk=order_id)
    components = Component.objects.filter(order=order)
    
    if not components.exists():
        messages.error(request, "The selected order has no components to invoice.")
        return redirect('invoices:select_order')
    
    if request.method == 'POST':
        form = BulkInvoiceForm(request.POST, order=order)
        attachment_formset = InvoiceAttachmentFormSet(request.POST, request.FILES, prefix='attachments')
        
        if form.is_valid() and attachment_formset.is_valid():
            # Create invoice
            invoice = Invoice.objects.create(
                invoice_number=form.cleaned_data['invoice_number'],
                invoice_date=form.cleaned_data['invoice_date'],
                company_name=form.cleaned_data['company_name'],
                notes=form.cleaned_data['notes'],
                created_by=request.user
            )
            
            # Create invoice components
            for component in form.cleaned_data['components']:
                InvoiceComponent.objects.create(
                    invoice=invoice,
                    component=component,
                    name=component.name,
                    value=component.value,
                    package=component.package,
                    part_number=component.part_number,
                    quantity=component.quantity,
                    price_per_unit=form.cleaned_data['price_per_unit'],
                    gst_percentage=form.cleaned_data['gst_percentage'],
                    warranty_information=form.cleaned_data['warranty_information']
                )
            
            # Save attachments
            attachment_instances = attachment_formset.save(commit=False)
            for attachment in attachment_instances:
                attachment.invoice = invoice
                attachment.uploaded_by = request.user
                attachment.save()
            
            messages.success(request, f"Bulk invoice {invoice.invoice_number} has been created successfully.")
            return redirect('invoices:detail', invoice_id=invoice.id)
    else:
        form = BulkInvoiceForm(order=order, initial={'components': components})
        attachment_formset = InvoiceAttachmentFormSet(prefix='attachments')
    
    context = {
        'form': form,
        'attachment_formset': attachment_formset,
        'order': order,
        'components': components,
        'title': f'Create Bulk Invoice for Order {order.order_id}'
    }
    return render(request, 'invoices/bulk_invoice_form.html', context)

@login_required
def select_components(request, order_id):
    """
    Select components from an order to create an invoice.
    Redirects to the invoice creation page with the selected components.
    """
    order = get_object_or_404(Order, pk=order_id)
    components = Component.objects.filter(order=order)
    
    if not components.exists():
        messages.error(request, "The selected order has no components to invoice.")
        return redirect('invoices:select_order')
    
    if request.method == 'POST':
        selected_component_ids = request.POST.getlist('component')
        
        if not selected_component_ids:
            messages.error(request, "Please select at least one component.")
            return HttpResponseRedirect(request.path_info)
        
        # Store selected components in session for the next step
        request.session['selected_component_ids'] = selected_component_ids
        request.session['order_id'] = order_id
        
        return redirect('invoices:create_from_components')
    
    context = {
        'order': order,
        'components': components,
        'title': f'Select Components from Order {order.order_id}'
    }
    return render(request, 'invoices/select_components.html', context)

@login_required
@transaction.atomic
def create_invoice_from_components(request):
    """
    Create an invoice from previously selected components.
    """
    # Get data from session
    selected_component_ids = request.session.get('selected_component_ids', [])
    order_id = request.session.get('order_id')
    
    if not selected_component_ids or not order_id:
        messages.error(request, "No components selected. Please start over.")
        return redirect('invoices:select_order')
    
    order = get_object_or_404(Order, pk=order_id)
    selected_components = Component.objects.filter(id__in=selected_component_ids, order=order)
    
    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        attachment_formset = InvoiceAttachmentFormSet(request.POST, request.FILES, prefix='attachments')
        
        # Create a dictionary to hold component forms data
        component_forms_valid = True
        component_data = {}
        
        # Process each component form
        for component in selected_components:
            prefix = f"component_{component.id}"
            price = request.POST.get(f"{prefix}-price_per_unit")
            quantity = request.POST.get(f"{prefix}-quantity")
            gst = request.POST.get(f"{prefix}-gst_percentage")
            warranty = request.POST.get(f"{prefix}-warranty_information", "")
            
            # Simple validation (in a real app, you'd use proper forms)
            if not price or not quantity or not gst:
                component_forms_valid = False
                break
                
            component_data[component.id] = {
                'price_per_unit': price,
                'quantity': quantity,
                'gst_percentage': gst,
                'warranty_information': warranty
            }
        
        if form.is_valid() and attachment_formset.is_valid() and component_forms_valid:
            # Create invoice
            invoice = form.save(commit=False)
            invoice.created_by = request.user
            invoice.save()
            
            # Create invoice components
            for component in selected_components:
                data = component_data[component.id]
                InvoiceComponent.objects.create(
                    invoice=invoice,
                    component=component,
                    name=component.name,
                    value=component.value,
                    package=component.package,
                    part_number=component.part_number,
                    quantity=data['quantity'],
                    price_per_unit=data['price_per_unit'],
                    gst_percentage=data['gst_percentage'],
                    warranty_information=data['warranty_information']
                )
            
            # Save attachments
            attachment_instances = attachment_formset.save(commit=False)
            for attachment in attachment_instances:
                attachment.invoice = invoice
                attachment.uploaded_by = request.user
                attachment.save()
            
            # Clear session data
            if 'selected_component_ids' in request.session:
                del request.session['selected_component_ids']
            if 'order_id' in request.session:
                del request.session['order_id']
            
            messages.success(request, f"Invoice {invoice.invoice_number} has been created successfully.")
            return redirect('invoices:detail', invoice_id=invoice.id)
    else:
        form = InvoiceForm()
        attachment_formset = InvoiceAttachmentFormSet(prefix='attachments')
    
    context = {
        'form': form,
        'attachment_formset': attachment_formset,
        'selected_components': selected_components,
        'order': order,
        'title': f'Create Invoice from Selected Components'
    }
    return render(request, 'invoices/component_invoice_form.html', context)

@login_required
def delete_invoice(request, invoice_id):
    """
    Delete an invoice.
    """
    invoice = get_object_or_404(Invoice, pk=invoice_id)
    
    if request.method == 'POST':
        invoice_number = invoice.invoice_number
        invoice.delete()
        messages.success(request, f"Invoice {invoice_number} has been deleted.")
        return redirect('invoices:list')
    
    context = {
        'invoice': invoice,
        'title': f'Delete Invoice {invoice.invoice_number}'
    }
    return render(request, 'invoices/invoice_confirm_delete.html', context)
