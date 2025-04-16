from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('', views.order_list, name='list'),
    path('create/', views.order_create, name='create'),
    path('<int:order_id>/', views.order_detail, name='detail'),
    path('<int:order_id>/edit/', views.order_update, name='update'),
    path('<int:order_id>/delete/', views.delete_order, name='delete'),
    path('<int:order_id>/status/', views.update_order_status, name='update_status'),
    path('component/<int:component_id>/status/', views.update_component_status, name='update_component_status'),
] 