from django.urls import path
from . import views

app_name = 'invoices'

urlpatterns = [
    # Invoice management
    path('', views.invoice_list, name='list'),
    path('create/', views.invoice_create, name='create'),
    path('<int:invoice_id>/', views.invoice_detail, name='detail'),
    path('<int:invoice_id>/update/', views.invoice_update, name='update'),
    path('<int:invoice_id>/delete/', views.delete_invoice, name='delete'),
    
    # Order-based invoice creation process
    path('select-order/', views.select_order_for_invoice, name='select_order'),
    path('order/<int:order_id>/bulk-invoice/', views.create_bulk_invoice, name='create_bulk_invoice'),
    path('order/<int:order_id>/select-components/', views.select_components, name='select_components'),
    path('from-components/', views.create_invoice_from_components, name='create_from_components'),
] 