from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from collections import Counter

class Order(models.Model):
    """
    Represents an order in the inventory management system.
    Tracks items from order placement to completion.
    """
    # Order Status Choices
    STATUS_REQUESTED = 'requested'
    STATUS_PLACED = 'placed'
    STATUS_IN_TRANSIT = 'in_transit'
    STATUS_RECEIVED = 'received'
    STATUS_QC = 'qc'
    STATUS_QC_FAILED = 'qc_failed'
    STATUS_QC_SUCCESSFUL = 'qc_successful'
    STATUS_HANDOVER = 'handover'
    STATUS_COMPLETED = 'completed'
    
    STATUS_CHOICES = [
        (STATUS_REQUESTED, _('Order Requested')),
        (STATUS_PLACED, _('Order Placed')),
        (STATUS_IN_TRANSIT, _('Material in Transit')),
        (STATUS_RECEIVED, _('Material Received')),
        (STATUS_QC, _('Material QC')),
        (STATUS_QC_FAILED, _('Material QC Failed')),
        (STATUS_QC_SUCCESSFUL, _('Material QC Successful')),
        (STATUS_HANDOVER, _('Material Handover')),
        (STATUS_COMPLETED, _('Order Completed')),
    ]
    
    # Map for status priority (lower number is higher priority)
    STATUS_PRIORITY = {
        STATUS_REQUESTED: 1,
        STATUS_PLACED: 2,
        STATUS_IN_TRANSIT: 3,
        STATUS_RECEIVED: 4,
        STATUS_QC: 5,
        STATUS_QC_FAILED: 6,
        STATUS_QC_SUCCESSFUL: 7,
        STATUS_HANDOVER: 8,
        STATUS_COMPLETED: 9,
    }
    
    # Order Fields
    order_id = models.CharField(_('Order ID'), max_length=50, unique=True, editable=False)
    request_id = models.CharField(_('Request ID'), max_length=50, blank=True, null=True)
    requested_amount = models.DecimalField(_('Requested Amount'), max_digits=12, decimal_places=2, default=0)
    actual_amount = models.DecimalField(_('Actual Amount'), max_digits=12, decimal_places=2, default=0)
    request_person = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='requested_orders',
        verbose_name=_('Request Person')
    )
    requested_team = models.ForeignKey(
        'accounts.Team',
        on_delete=models.PROTECT,
        related_name='team_orders',
        verbose_name=_('Requested Team')
    )
    
    # Status tracking
    status = models.CharField(
        _('Status'),
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_REQUESTED
    )
    
    # Timestamps
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)
    completed_at = models.DateTimeField(_('Completed At'), null=True, blank=True)
    
    # Metadata
    notes = models.TextField(_('Notes'), blank=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')
    
    def __str__(self):
        return f"Order {self.order_id}"
    
    def save(self, *args, **kwargs):
        # Generate order_id if not provided
        if not self.order_id:
            # Format: ORD-{year}{month}{day}-{random_number}
            from django.utils import timezone
            import random
            today = timezone.now()
            random_number = random.randint(1000, 9999)
            self.order_id = f"ORD-{today.strftime('%Y%m%d')}-{random_number}"
        
        # Update status based on component statuses if components exist
        if hasattr(self, 'pk') and self.pk:
            self.update_status_from_components()
            
        super().save(*args, **kwargs)
    
    def update_status_from_components(self):
        """
        Updates the order status based on the mode of component statuses.
        If multiple modes exist, selects the status with the lowest priority value.
        """
        components = self.components.all()
        if components.exists():
            # Get all component statuses
            component_statuses = components.values_list('status', flat=True)
            
            # Find most common status (mode)
            status_counter = Counter(component_statuses)
            most_common_statuses = status_counter.most_common()
            
            # Get the highest count
            highest_count = most_common_statuses[0][1]
            
            # Find all statuses with that count (multiple modes)
            modes = [status for status, count in most_common_statuses if count == highest_count]
            
            if len(modes) == 1:
                # Single mode, use it
                self.status = modes[0]
            elif len(modes) > 1:
                # Multiple modes, get the one with lowest priority number
                self.status = min(modes, key=lambda x: self.STATUS_PRIORITY.get(x, 99))


class Component(models.Model):
    """
    Represents a component within an order.
    """
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='components',
        verbose_name=_('Order')
    )
    name = models.CharField(_('Name'), max_length=255)
    value = models.CharField(_('Value'), max_length=255, blank=True)
    package = models.CharField(_('Package'), max_length=255, blank=True)
    part_number = models.CharField(_('Part Number'), max_length=255, blank=True)
    quantity = models.PositiveIntegerField(_('Quantity'), default=1)
    links = models.TextField(_('Links'), blank=True)
    due_date = models.DateField(_('Due Date'), null=True, blank=True)
    comments = models.TextField(_('Comments'), blank=True)
    
    # Component Status
    status = models.CharField(
        _('Status'),
        max_length=20,
        choices=Order.STATUS_CHOICES,
        default=Order.STATUS_REQUESTED
    )
    
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)
    
    class Meta:
        ordering = ['name']
        verbose_name = _('Component')
        verbose_name_plural = _('Components')
    
    def __str__(self):
        return f"{self.name} - {self.part_number}"
    
    def save(self, *args, **kwargs):
        # Save the component
        super().save(*args, **kwargs)
        
        # Update the parent order's status
        self.order.update_status_from_components()
        self.order.save(update_fields=['status'])


class OrderStatusHistory(models.Model):
    """
    Tracks the history of status changes for an order.
    """
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='status_history',
        verbose_name=_('Order')
    )
    status = models.CharField(_('Status'), max_length=20, choices=Order.STATUS_CHOICES)
    changed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='status_changes',
        verbose_name=_('Changed By')
    )
    changed_at = models.DateTimeField(_('Changed At'), auto_now_add=True)
    notes = models.TextField(_('Notes'), blank=True)
    
    class Meta:
        ordering = ['-changed_at']
        verbose_name = _('Order Status History')
        verbose_name_plural = _('Order Status History')
    
    def __str__(self):
        return f"{self.order.order_id} - {self.get_status_display()}"
