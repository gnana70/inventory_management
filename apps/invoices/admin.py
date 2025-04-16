from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Invoice, InvoiceComponent, InvoiceAttachment

class InvoiceComponentInline(admin.TabularInline):
    model = InvoiceComponent
    extra = 0
    fields = ('component', 'name', 'part_number', 'quantity', 'price_per_unit', 'gst_percentage', 'subtotal', 'gst_amount', 'total_value_including_gst', 'warranty_information')
    readonly_fields = ('subtotal', 'gst_amount', 'total_value_including_gst')
    autocomplete_fields = ['component']
    
    def subtotal(self, obj):
        if obj.pk:
            return obj.subtotal
        return '-'
    
    def gst_amount(self, obj):
        if obj.pk:
            return obj.gst_amount
        return '-'
    
    def total_value_including_gst(self, obj):
        if obj.pk:
            return obj.total_value_including_gst
        return '-'

class InvoiceAttachmentInline(admin.TabularInline):
    model = InvoiceAttachment
    extra = 0
    fields = ('file', 'description', 'uploaded_by', 'uploaded_at')
    readonly_fields = ('uploaded_at',)

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'company_name', 'invoice_date', 'created_by', 'total_value', 'created_at')
    list_filter = ('invoice_date', 'company_name', 'created_at')
    search_fields = ('invoice_number', 'company_name', 'notes', 'invoice_components__name', 'invoice_components__part_number')
    date_hierarchy = 'invoice_date'
    readonly_fields = ('created_at', 'updated_at', 'total_value')
    fieldsets = (
        (None, {
            'fields': ('invoice_number', 'invoice_date', 'company_name')
        }),
        (_('Additional Information'), {
            'fields': ('notes',)
        }),
        (_('System Information'), {
            'fields': ('created_by', 'created_at', 'updated_at', 'total_value'),
            'classes': ('collapse',)
        }),
    )
    inlines = [InvoiceComponentInline, InvoiceAttachmentInline]
    
    def save_model(self, request, obj, form, change):
        if not change:  # If creating new object
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
    
    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            if isinstance(instance, InvoiceAttachment) and not instance.uploaded_by_id:
                instance.uploaded_by = request.user
            instance.save()
        formset.save_m2m()
        
    def total_value(self, obj):
        return obj.total_value
    total_value.short_description = _('Total Value')

@admin.register(InvoiceComponent)
class InvoiceComponentAdmin(admin.ModelAdmin):
    list_display = ('name', 'part_number', 'invoice', 'component', 'quantity', 'price_per_unit', 'gst_percentage', 'total_value_including_gst')
    list_filter = ('invoice__invoice_date', 'gst_percentage')
    search_fields = ('name', 'part_number', 'invoice__invoice_number', 'component__name', 'component__part_number')
    autocomplete_fields = ['invoice', 'component']
    readonly_fields = ('created_at', 'updated_at', 'subtotal', 'gst_amount', 'total_value_including_gst')
    fieldsets = (
        (None, {
            'fields': ('invoice', 'component')
        }),
        (_('Component Details'), {
            'fields': ('name', 'value', 'package', 'part_number')
        }),
        (_('Pricing Details'), {
            'fields': ('quantity', 'price_per_unit', 'gst_percentage', 'subtotal', 'gst_amount', 'total_value_including_gst', 'warranty_information')
        }),
        (_('System Information'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def subtotal(self, obj):
        return obj.subtotal
    subtotal.short_description = _('Subtotal')
    
    def gst_amount(self, obj):
        return obj.gst_amount
    gst_amount.short_description = _('GST Amount')
    
    def total_value_including_gst(self, obj):
        return obj.total_value_including_gst
    total_value_including_gst.short_description = _('Total Value (incl. GST)')

@admin.register(InvoiceAttachment)
class InvoiceAttachmentAdmin(admin.ModelAdmin):
    list_display = ('filename', 'invoice', 'description', 'uploaded_by', 'uploaded_at')
    list_filter = ('uploaded_at', 'invoice__invoice_date')
    search_fields = ('description', 'invoice__invoice_number', 'file')
    autocomplete_fields = ['invoice', 'uploaded_by']
    readonly_fields = ('uploaded_at', 'filename')
    
    def filename(self, obj):
        return obj.filename
    filename.short_description = _('Filename')
