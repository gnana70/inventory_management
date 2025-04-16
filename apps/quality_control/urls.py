from django.urls import path
from . import views

app_name = 'quality_control'

urlpatterns = [
    # QC Dashboard and listings
    path('', views.qc_dashboard, name='dashboard'),
    path('components/', views.qc_components_list, name='component_list'),
    
    # Order-specific QC
    path('order/<int:order_id>/', views.order_qc_list, name='order_components'),
    path('order/<int:order_id>/bulk-update/', views.bulk_qc_update, name='bulk_update'),
    
    # Component-specific QC
    path('component/<int:component_id>/', views.component_qc_update, name='component_update'),
] 