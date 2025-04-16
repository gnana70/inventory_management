from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, FileExtensionValidator

class Invoice(models.Model):
    """
    Represents an invoice that can cover one or multiple components across orders.
    """
    invoice_number = models.CharField(_('Invoice Number'), max_length=100, unique=True)
    invoice_date = models.DateField(_('Invoice Date'))
    company_name = models.CharField(_('Company/Vendor Name'), max_length=255)
    
    # Metadata
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='created_invoices',
        verbose_name=_('Created By')
    )
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)
    notes = models.TextField(_('Notes'), blank=True)
    
    class Meta:
        ordering = ['-invoice_date', 'invoice_number']
        verbose_name = _('Invoice')
        verbose_name_plural = _('Invoices')
    
    def __str__(self):
        return f"Invoice {self.invoice_number} - {self.company_name}"
    
    @property
    def total_value(self):
        """Calculate the total value of the invoice including GST."""
        return sum(component.total_value_including_gst for component in self.invoice_components.all())


class InvoiceComponent(models.Model):
    """
    Represents a component within an invoice.
    Links the invoice to an order component and stores pricing details.
    """
    invoice = models.ForeignKey(
        Invoice,
        on_delete=models.CASCADE,
        related_name='invoice_components',
        verbose_name=_('Invoice')
    )
    component = models.ForeignKey(
        'orders.Component',
        on_delete=models.PROTECT,
        related_name='invoice_entries',
        verbose_name=_('Component')
    )
    
    # Component details as they appear in the invoice
    name = models.CharField(_('Name'), max_length=255)
    value = models.CharField(_('Value'), max_length=255, blank=True)
    package = models.CharField(_('Package'), max_length=255, blank=True)
    part_number = models.CharField(_('Part Number'), max_length=255, blank=True)
    
    # Invoice-specific information
    quantity = models.PositiveIntegerField(_('Quantity'), validators=[MinValueValidator(1)])
    price_per_unit = models.DecimalField(_('Price Per Unit'), max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    gst_percentage = models.DecimalField(_('GST Percentage'), max_digits=5, decimal_places=2, default=18.00)
    warranty_information = models.CharField(_('Warranty Information'), max_length=255, blank=True)
    
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)
    
    class Meta:
        ordering = ['name']
        verbose_name = _('Invoice Component')
        verbose_name_plural = _('Invoice Components')
        # Ensure a component can only appear once per invoice
        unique_together = ['invoice', 'component']
    
    def __str__(self):
        return f"{self.name} - {self.part_number}"
    
    @property
    def subtotal(self):
        """Calculate the subtotal (price × quantity) before GST."""
        return self.price_per_unit * self.quantity
    
    @property
    def gst_amount(self):
        """Calculate the GST amount."""
        return (self.price_per_unit * self.quantity) * (self.gst_percentage / 100)
    
    @property
    def total_value_including_gst(self):
        """Calculate the total value including GST."""
        return self.subtotal + self.gst_amount
    
    def save(self, *args, **kwargs):
        """
        Pre-populate component details from the linked Component if not provided.
        """
        if not self.name and self.component:
            self.name = self.component.name
        if not self.value and self.component:
            self.value = self.component.value
        if not self.package and self.component:
            self.package = self.component.package
        if not self.part_number and self.component:
            self.part_number = self.component.part_number
            
        super().save(*args, **kwargs)


class InvoiceAttachment(models.Model):
    """
    Represents a file attachment for an invoice.
    """
    invoice = models.ForeignKey(
        Invoice,
        on_delete=models.CASCADE,
        related_name='attachments',
        verbose_name=_('Invoice')
    )
    file = models.FileField(
        _('File'),
        upload_to='invoices/attachments/%Y/%m/',
        validators=[
            FileExtensionValidator(allowed_extensions=['pdf', 'jpg', 'jpeg', 'png', 'doc', 'docx', 'xls', 'xlsx'])
        ]
    )
    description = models.CharField(_('Description'), max_length=255, blank=True)
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='invoice_attachments',
        verbose_name=_('Uploaded By')
    )
    uploaded_at = models.DateTimeField(_('Uploaded At'), auto_now_add=True)
    
    class Meta:
        ordering = ['-uploaded_at']
        verbose_name = _('Invoice Attachment')
        verbose_name_plural = _('Invoice Attachments')
    
    def __str__(self):
        return f"Attachment for {self.invoice.invoice_number} - {self.description}"
    
    @property
    def filename(self):
        """Return the filename of the attachment."""
        return self.file.name.split('/')[-1]
