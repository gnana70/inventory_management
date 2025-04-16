from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.forms import modelformset_factory
from django.db import transaction
from django.http import JsonResponse

from .models import Order, Component, OrderStatusHistory
from .forms import OrderForm, ComponentForm, OrderFilterForm

@login_required
def order_list(request):
    """
    Display a list of orders with filtering options.
    """
    filter_form = OrderFilterForm(request.GET)
    orders = Order.objects.all().select_related('request_person', 'requested_team')
    
    # Apply filters if the form is valid
    if filter_form.is_valid():
        data = filter_form.cleaned_data
        if data.get('status'):
            orders = orders.filter(status=data['status'])
        if data.get('requested_team'):
            orders = orders.filter(requested_team=data['requested_team'])
        if data.get('request_person'):
            orders = orders.filter(request_person=data['request_person'])
        if data.get('date_from'):
            orders = orders.filter(created_at__gte=data['date_from'])
        if data.get('date_to'):
            orders = orders.filter(created_at__lte=data['date_to'])
        if data.get('search'):
            search_term = data['search']
            orders = orders.filter(
                order_id__icontains=search_term
            ) | orders.filter(
                request_id__icontains=search_term
            ) | orders.filter(
                components__name__icontains=search_term
            ) | orders.filter(
                components__part_number__icontains=search_term
            ).distinct()
    
    context = {
        'orders': orders,
        'filter_form': filter_form,
    }
    return render(request, 'orders/order_list.html', context)

@login_required
def order_detail(request, order_id):
    """
    Display details of a specific order.
    """
    order = get_object_or_404(Order.objects.select_related('request_person', 'requested_team'), pk=order_id)
    components = order.components.all()
    status_history = order.status_history.all().select_related('changed_by')
    
    # Count components in QC state
    qc_components_count = components.filter(status=Order.STATUS_QC).count()
    
    context = {
        'order': order,
        'components': components,
        'status_history': status_history,
        'qc_components_count': qc_components_count,
        'title': f'Order: {order.order_id}'
    }
    
    return render(request, 'orders/order_detail.html', context)

@login_required
@transaction.atomic
def order_create(request):
    """
    Create a new order with components.
    """
    if request.method == 'POST':
        order_form = OrderForm(request.POST)
        component_formset = modelformset_factory(Component, form=ComponentForm, extra=1)(
            request.POST, prefix='components'
        )
        
        # Print received form data for debugging
        for key, value in request.POST.items():
            if 'status' in key:
                print(f"Form data: {key} = {value}")
        
        # Ensure all components have a status value
        for form in component_formset.forms:
            if form.is_valid() and 'status' not in form.cleaned_data:
                form.cleaned_data['status'] = Order.STATUS_REQUESTED
                form.instance.status = Order.STATUS_REQUESTED
        
        if order_form.is_valid() and component_formset.is_valid():
            # Create the order
            order = order_form.save(commit=False)
            order.request_person = request.user
            order.save()
            
            # Create status history entry
            OrderStatusHistory.objects.create(
                order=order,
                status=order.status,
                changed_by=request.user,
                notes="Order created"
            )
            
            # Save components
            components = component_formset.save(commit=False)
            for component in components:
                component.order = order
                # Ensure status is set if empty
                if not component.status:
                    component.status = Order.STATUS_REQUESTED
                component.save()
            
            messages.success(request, f"Order {order.order_id} has been created successfully.")
            return redirect('orders:detail', order_id=order.id)
        else:
            # Debug validation errors
            if not order_form.is_valid():
                for field, errors in order_form.errors.items():
                    messages.error(request, f"Order field '{field}': {', '.join(errors)}")
            
            if not component_formset.is_valid():
                for i, form in enumerate(component_formset):
                    if form.errors:
                        for field, errors in form.errors.items():
                            messages.error(request, f"Component #{i+1} field '{field}': {', '.join(errors)}")
                if component_formset.non_form_errors():
                    for error in component_formset.non_form_errors():
                        messages.error(request, f"Component formset error: {error}")
    else:
        order_form = OrderForm()
        component_formset = modelformset_factory(Component, form=ComponentForm, extra=1)(
            queryset=Component.objects.none(), prefix='components'
        )
    
    context = {
        'order_form': order_form,
        'component_formset': component_formset,
    }
    return render(request, 'orders/order_form.html', context)

@login_required
@transaction.atomic
def order_update(request, order_id):
    """
    Update an existing order and its components.
    """
    order = get_object_or_404(Order, pk=order_id)
    
    # Check if order can be edited (not completed)
    if order.status == Order.STATUS_COMPLETED:
        messages.error(request, "Completed orders cannot be edited.")
        return redirect('orders:detail', order_id=order.id)
    
    if request.method == 'POST':
        old_status = order.status
        order_form = OrderForm(request.POST, instance=order)
        
        # Print received form data for debugging
        for key, value in request.POST.items():
            if 'status' in key:
                print(f"Form data: {key} = {value}")
        
        # Create component formset with explicit initial values for status
        component_formset = modelformset_factory(
            Component, 
            form=ComponentForm, 
            extra=1, 
            can_delete=True
        )(
            request.POST, 
            prefix='components', 
            queryset=order.components.all()
        )
        
        # Ensure all components have a status value
        for form in component_formset.forms:
            if hasattr(form, 'cleaned_data'):
                if form.is_valid() and 'status' not in form.cleaned_data:
                    form.cleaned_data['status'] = Order.STATUS_REQUESTED
                    form.instance.status = Order.STATUS_REQUESTED
                
                # For debugging
                if not form.is_valid():
                    print(f"Form errors: {form.errors}")
        
        # Log complete form data for debugging
        print(f"Order form is valid: {order_form.is_valid()}")
        print(f"Component formset is valid: {component_formset.is_valid()}")
        
        if order_form.is_valid() and component_formset.is_valid():
            # Update the order
            order = order_form.save()
            
            # Check if status changed
            if old_status != order.status:
                # Create status history entry
                OrderStatusHistory.objects.create(
                    order=order,
                    status=order.status,
                    changed_by=request.user,
                    notes=request.POST.get('status_notes', '')
                )
                
                # If completed, set completed_at
                if order.status == Order.STATUS_COMPLETED and not order.completed_at:
                    order.completed_at = timezone.now()
                    order.save()
            
            # Save components
            components = component_formset.save(commit=False)
            for component in components:
                component.order = order
                # Ensure status is set if empty
                if not component.status:
                    component.status = Order.STATUS_REQUESTED
                component.save()
            
            # Delete components marked for deletion
            for obj in component_formset.deleted_objects:
                obj.delete()
            
            messages.success(request, f"Order {order.order_id} has been updated successfully.")
            return redirect('orders:detail', order_id=order.id)
        else:
            # Debug validation errors
            if not order_form.is_valid():
                for field, errors in order_form.errors.items():
                    messages.error(request, f"Order field '{field}': {', '.join(errors)}")
            
            if not component_formset.is_valid():
                for i, form in enumerate(component_formset):
                    if form.errors:
                        for field, errors in form.errors.items():
                            messages.error(request, f"Component #{i+1} field '{field}': {', '.join(errors)}")
                if component_formset.non_form_errors():
                    for error in component_formset.non_form_errors():
                        messages.error(request, f"Component formset error: {error}")
    else:
        order_form = OrderForm(instance=order)
        component_formset = modelformset_factory(Component, form=ComponentForm, extra=1, can_delete=True)(
            queryset=order.components.all(), prefix='components'
        )
    
    context = {
        'order_form': order_form,
        'component_formset': component_formset,
        'order': order,
    }
    return render(request, 'orders/order_form.html', context)

@login_required
def update_order_status(request, order_id):
    """
    Update the status of an order via AJAX.
    """
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        order = get_object_or_404(Order, pk=order_id)
        new_status = request.POST.get('status')
        notes = request.POST.get('notes', '')
        
        if new_status in dict(Order.STATUS_CHOICES).keys():
            old_status = order.status
            order.status = new_status
            
            # Set completed_at if status is completed
            if new_status == Order.STATUS_COMPLETED and not order.completed_at:
                order.completed_at = timezone.now()
            
            order.save()
            
            # Create status history entry
            OrderStatusHistory.objects.create(
                order=order,
                status=new_status,
                changed_by=request.user,
                notes=notes
            )
            
            return JsonResponse({
                'success': True,
                'message': f"Status updated from {dict(Order.STATUS_CHOICES)[old_status]} to {dict(Order.STATUS_CHOICES)[new_status]}",
                'status': dict(Order.STATUS_CHOICES)[new_status]
            })
        
        return JsonResponse({
            'success': False,
            'message': "Invalid status provided"
        })
    
    return JsonResponse({
        'success': False,
        'message': "Invalid request"
    })

@login_required
def update_component_status(request, component_id):
    """
    Update the status of a component via AJAX.
    """
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        component = get_object_or_404(Component, pk=component_id)
        new_status = request.POST.get('status')
        
        if new_status in dict(Order.STATUS_CHOICES).keys():
            old_status = component.status
            component.status = new_status
            component.save()
            
            # Order status will be automatically updated by the component's save method
            
            return JsonResponse({
                'success': True,
                'message': f"Component status updated from {dict(Order.STATUS_CHOICES)[old_status]} to {dict(Order.STATUS_CHOICES)[new_status]}",
                'status': dict(Order.STATUS_CHOICES)[new_status],
                'order_status': component.order.status,
                'order_status_display': dict(Order.STATUS_CHOICES)[component.order.status]
            })
        
        return JsonResponse({
            'success': False,
            'message': "Invalid status provided"
        })
    
    return JsonResponse({
        'success': False,
        'message': "Invalid request"
    })

@login_required
@transaction.atomic
def delete_order(request, order_id):
    """
    Delete an order and all its associated components.
    """
    order = get_object_or_404(Order, pk=order_id)
    
    if request.method == 'POST':
        order_id_display = order.order_id  # Save for the success message
        
        # Delete the order (cascades to components and status history)
        order.delete()
        
        messages.success(request, f"Order {order_id_display} has been deleted successfully.")
        return redirect('orders:list')
    
    context = {
        'order': order,
    }
    return render(request, 'orders/order_confirm_delete.html', context)
