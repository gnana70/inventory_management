from django.contrib import admin
from .models import QualityControlRecord

@admin.register(QualityControlRecord)
class QualityControlRecordAdmin(admin.ModelAdmin):
    list_display = ('component', 'status', 'inspector', 'inspection_date')
    list_filter = ('status', 'inspection_date', 'inspector')
    search_fields = ('component__name', 'component__part_number', 'component__order__order_id', 'comments')
    date_hierarchy = 'inspection_date'
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('component', 'status', 'inspector', 'inspection_date')
        }),
        ('Details', {
            'fields': ('comments',)
        }),
        ('System', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
