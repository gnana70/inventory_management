from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum, Q
from django.utils import timezone

# Import models
from apps.orders.models import Order, Component
from apps.invoices.models import Invoice
from apps.quality_control.models import QualityControlRecord


@login_required
def index(request):
    """Main dashboard view"""
    # Get actual data from the database
    
    # Orders statistics
    total_orders = Order.objects.count()
    pending_orders = Order.objects.exclude(status='completed').count()
    completed_orders = Order.objects.filter(status='completed').count()
    
    # Invoices count
    invoices_count = Invoice.objects.count()
    
    # QC pending count
    qc_pending = Component.objects.filter(status='qc').count()
    
    # Recent orders
    recent_orders = Order.objects.all().order_by('-created_at')[:5]
    
    # Orders by status
    status_counts = Order.objects.values('status').annotate(count=Count('id'))
    orders_by_status = []
    
    # Create a dictionary to map status values to display names
    status_map = dict(Order.STATUS_CHOICES)
    
    # Initialize all statuses with zero counts
    for status_code, status_name in Order.STATUS_CHOICES:
        orders_by_status.append({
            'name': status_name,
            'count': 0
        })
    
    # Update counts from the database
    for item in status_counts:
        for i, status_data in enumerate(orders_by_status):
            if status_data['name'] == status_map.get(item['status']):
                orders_by_status[i]['count'] = item['count']
                break
    
    context = {
        'orders_count': total_orders,
        'orders_pending': pending_orders,
        'orders_completed': completed_orders,
        'invoices_count': invoices_count,
        'qc_pending': qc_pending,
        'recent_orders': recent_orders,
        'orders_by_status': orders_by_status,
    }
    return render(request, 'dashboard/index.html', context)


@login_required
def reports(request):
    """Reports dashboard"""
    context = {
        'reports': [
            {'name': 'Orders by Status', 'url': '#'},
            {'name': 'Orders by Team', 'url': '#'},
            {'name': 'Orders by Month', 'url': '#'},
            {'name': 'Invoices Summary', 'url': '#'},
            {'name': 'Quality Control Report', 'url': '#'},
        ]
    }
    return render(request, 'dashboard/reports.html', context)


@login_required
def search(request):
    """Global search functionality"""
    query = request.GET.get('q', '')
    results = {
        'orders': [],
        'invoices': [],
        'users': [],
    }
    
    if query:
        # Perform search using actual models
        orders = Order.objects.filter(
            Q(order_id__icontains=query) | 
            Q(request_id__icontains=query) |
            Q(notes__icontains=query)
        )[:10]
        
        invoices = Invoice.objects.filter(
            Q(invoice_number__icontains=query) |
            Q(company_name__icontains=query) |
            Q(notes__icontains=query)
        )[:10]
        
        results['orders'] = orders
        results['invoices'] = invoices
    
    context = {
        'query': query,
        'results': results,
    }
    return render(request, 'dashboard/search_results.html', context)
