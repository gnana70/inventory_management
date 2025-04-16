from django.contrib import admin
from .models import Order, Component, OrderStatusHistory

class ComponentInline(admin.TabularInline):
    model = Component
    extra = 1
    fields = ('name', 'value', 'package', 'part_number', 'quantity', 'due_date', 'status')

class OrderStatusHistoryInline(admin.TabularInline):
    model = OrderStatusHistory
    extra = 0
    fields = ('status', 'changed_by', 'changed_at', 'notes')
    readonly_fields = ('changed_at',)
    can_delete = False
    
    def has_add_permission(self, request, obj=None):
        return False

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'request_id', 'status', 'request_person', 'requested_team', 'created_at')
    list_filter = ('status', 'requested_team', 'created_at')
    search_fields = ('order_id', 'request_id', 'request_person__username', 'request_person__email')
    readonly_fields = ('order_id', 'created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('order_id', 'request_id', 'status')
        }),
        ('Financial Information', {
            'fields': ('requested_amount', 'actual_amount')
        }),
        ('Request Details', {
            'fields': ('request_person', 'requested_team')
        }),
        ('Additional Information', {
            'fields': ('notes', 'created_at', 'updated_at', 'completed_at')
        }),
    )
    inlines = [ComponentInline, OrderStatusHistoryInline]

@admin.register(Component)
class ComponentAdmin(admin.ModelAdmin):
    list_display = ('name', 'part_number', 'order', 'quantity', 'due_date', 'status')
    list_filter = ('due_date', 'status')
    search_fields = ('name', 'part_number', 'order__order_id')
    autocomplete_fields = ('order',)
