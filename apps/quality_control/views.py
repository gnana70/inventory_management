from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.utils.translation import gettext_lazy as _
from django.http import JsonResponse
from django.urls import reverse

from apps.orders.models import Order, Component
from .models import QualityControlRecord
from .forms import QualityControlRecordForm, ComponentQCUpdateForm

@login_required
def qc_dashboard(request):
    """
    Dashboard view displaying orders with components in QC state
    """
    # Find orders that have components in QC state
    orders_with_qc = Order.objects.filter(
        components__status=Order.STATUS_QC
    ).distinct().order_by('-created_at')
    
    # Calculate QC component counts for each order
    orders_with_counts = []
    for order in orders_with_qc:
        qc_count = order.components.filter(status=Order.STATUS_QC).count()
        orders_with_counts.append({
            'order': order,
            'qc_count': qc_count
        })
    
    context = {
        'orders_with_counts': orders_with_counts,
        'title': _('Quality Control Dashboard')
    }
    return render(request, 'quality_control/dashboard.html', context)

@login_required
def order_qc_list(request, order_id):
    """
    List all components in QC state for a specific order
    """
    order = get_object_or_404(Order, pk=order_id)
    
    # Get components in QC state for this order
    components = Component.objects.filter(
        order=order,
        status=Order.STATUS_QC
    ).order_by('name')
    
    context = {
        'order': order,
        'components': components,
        'title': _('QC Components for Order {0}').format(order.order_id)
    }
    return render(request, 'quality_control/component_list.html', context)

@login_required
@transaction.atomic
def component_qc_update(request, component_id):
    """
    Update the QC status of a specific component
    """
    component = get_object_or_404(Component, pk=component_id)
    
    # Check if the component is in QC state
    if component.status != Order.STATUS_QC:
        messages.error(request, _('This component is not in QC state.'))
        return redirect('orders:detail', order_id=component.order.id)
    
    if request.method == 'POST':
        form = ComponentQCUpdateForm(request.POST)
        if form.is_valid():
            # Create QC record
            qc_record = QualityControlRecord(
                component=component,
                status=form.cleaned_data['status'],
                comments=form.cleaned_data['comments'],
                inspector=request.user
            )
            qc_record.save()  # This also updates the component status
            
            # Update order status if needed
            component.order.update_status_from_components()
            component.order.save()
            
            messages.success(request, _('Quality control status has been updated successfully.'))
            
            # Redirect to the order detail page
            return redirect('orders:detail', order_id=component.order.id)
    else:
        form = ComponentQCUpdateForm()
    
    context = {
        'form': form,
        'component': component,
        'order': component.order,
        'title': _('Update QC Status for {0}').format(component.name)
    }
    return render(request, 'quality_control/component_qc_form.html', context)

@login_required
def qc_components_list(request):
    """
    List all components in QC state across all orders
    """
    # Get all components in QC state
    components = Component.objects.filter(
        status=Order.STATUS_QC
    ).select_related('order').order_by('order__order_id', 'name')
    
    context = {
        'components': components,
        'title': _('Components in QC State')
    }
    return render(request, 'quality_control/all_components.html', context)

@login_required
@transaction.atomic
def bulk_qc_update(request, order_id):
    """
    Bulk update QC status for multiple components in an order
    """
    order = get_object_or_404(Order, pk=order_id)
    
    # Get components in QC state for this order
    qc_components = Component.objects.filter(
        order=order,
        status=Order.STATUS_QC
    ).order_by('name')
    
    if not qc_components.exists():
        messages.warning(request, _('No components are in QC state for this order.'))
        return redirect('orders:detail', order_id=order.id)
    
    if request.method == 'POST':
        # Process each component
        updated_count = 0
        for component in qc_components:
            component_prefix = f"component_{component.id}"
            status = request.POST.get(f"{component_prefix}_status")
            comments = request.POST.get(f"{component_prefix}_comments", "")
            
            if status in [QualityControlRecord.STATUS_PASSED, QualityControlRecord.STATUS_FAILED]:
                qc_record = QualityControlRecord(
                    component=component,
                    status=status,
                    comments=comments,
                    inspector=request.user
                )
                qc_record.save()  # This also updates the component status
                updated_count += 1
        
        if updated_count > 0:
            # Update order status
            order.update_status_from_components()
            order.save()
            
            messages.success(
                request, 
                _('QC status updated for {0} components.').format(updated_count)
            )
            return redirect('orders:detail', order_id=order.id)
        else:
            messages.error(request, _('No components were updated. Please select a status for at least one component.'))
    
    context = {
        'order': order,
        'components': qc_components,
        'title': _('Bulk QC Update for Order {0}').format(order.order_id)
    }
    return render(request, 'quality_control/bulk_qc_form.html', context)
