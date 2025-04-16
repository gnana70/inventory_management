from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from apps.orders.models import Component, Order

class QualityControlRecord(models.Model):
    """
    Represents a quality control record for a component.
    Tracks the QC status, comments, and personnel responsible.
    """
    # Status choices
    STATUS_PASSED = 'passed'
    STATUS_FAILED = 'failed'
    
    STATUS_CHOICES = [
        (STATUS_PASSED, _('QC Successful')),
        (STATUS_FAILED, _('QC Failed')),
    ]
    
    component = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        related_name='qc_records',
        verbose_name=_('Component')
    )
    status = models.CharField(
        _('QC Status'),
        max_length=20,
        choices=STATUS_CHOICES
    )
    comments = models.TextField(_('Comments'), blank=True)
    inspector = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='qc_records',
        verbose_name=_('Inspector')
    )
    inspection_date = models.DateTimeField(_('Inspection Date'), default=timezone.now)
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)
    
    class Meta:
        ordering = ['-inspection_date']
        verbose_name = _('Quality Control Record')
        verbose_name_plural = _('Quality Control Records')
    
    def __str__(self):
        return f"QC for {self.component} - {self.get_status_display()}"
    
    def save(self, *args, **kwargs):
        # Save the QC record
        super().save(*args, **kwargs)
        
        # Update the component's status based on QC result
        if self.status == self.STATUS_PASSED:
            self.component.status = Order.STATUS_QC_SUCCESSFUL
        elif self.status == self.STATUS_FAILED:
            self.component.status = Order.STATUS_QC_FAILED
        
        self.component.save(update_fields=['status'])
