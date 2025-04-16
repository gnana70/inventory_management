# Inventory Management System - Modular Code Structure

## Overview

This document outlines the modular code structure for the Inventory Management System Django project. The structure is designed to ensure code maintainability, readability, and scalability while keeping individual files under 500 lines of code.

## Project Structure

```
inventory_management/
├── config/                          # Project configuration
│   ├── settings/                    # Split settings
│   │   ├── __init__.py
│   │   ├── base.py                  # Base settings shared by all environments
│   │   ├── development.py           # Development-specific settings
│   │   ├── production.py            # Production-specific settings
│   │   └── test.py                  # Test-specific settings
│   ├── urls.py                      # Main URL routing
│   ├── wsgi.py                      # WSGI config
│   └── asgi.py                      # ASGI config
│
├── apps/                            # Django applications
│   ├── accounts/                    # User management app
│   │   ├── api/                     # API related code
│   │   │   ├── __init__.py
│   │   │   ├── serializers.py
│   │   │   ├── urls.py
│   │   │   └── views.py
│   │   ├── management/
│   │   │   └── commands/            # Custom management commands
│   │   ├── migrations/              # Database migrations
│   │   ├── templates/               # Templates specific to accounts
│   │   │   └── accounts/
│   │   ├── tests/                   # Tests split by functionality
│   │   │   ├── __init__.py
│   │   │   ├── test_models.py
│   │   │   ├── test_forms.py
│   │   │   └── test_views.py
│   │   ├── __init__.py
│   │   ├── admin.py                 # Admin site configuration
│   │   ├── apps.py                  # App configuration
│   │   ├── forms.py                 # Forms for user input
│   │   ├── models.py                # Data models (split if needed)
│   │   ├── services.py              # Business logic
│   │   ├── urls.py                  # URL patterns for the app
│   │   └── views.py                 # View controllers
│   │
│   ├── orders/                      # Orders management app
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── serializers/         # Split serializers by entity
│   │   │   │   ├── __init__.py
│   │   │   │   ├── order.py
│   │   │   │   └── component.py
│   │   │   ├── urls.py
│   │   │   └── views/               # Split views by entity
│   │   │       ├── __init__.py
│   │   │       ├── order.py
│   │   │       └── component.py
│   │   ├── migrations/
│   │   ├── models/                  # Split models by entity
│   │   │   ├── __init__.py
│   │   │   ├── order.py
│   │   │   ├── component.py
│   │   │   └── status.py
│   │   ├── services/                # Split services by functionality
│   │   │   ├── __init__.py
│   │   │   ├── order_service.py
│   │   │   └── status_service.py
│   │   ├── templates/
│   │   │   └── orders/
│   │   │       ├── list.html
│   │   │       ├── detail.html
│   │   │       └── components/      # Reusable template components
│   │   │           ├── order_form.html
│   │   │           └── status_timeline.html
│   │   ├── tests/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── forms/                   # Split forms by entity
│   │   │   ├── __init__.py
│   │   │   ├── order.py
│   │   │   └── component.py
│   │   ├── urls.py
│   │   └── views/                   # Split views by functionality
│   │       ├── __init__.py
│   │       ├── order.py
│   │       └── component.py
│   │
│   ├── invoices/                    # Invoices management app
│   │   ├── api/
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── invoice.py
│   │   │   ├── component.py
│   │   │   └── attachment.py
│   │   ├── services/
│   │   ├── templates/
│   │   └── ...
│   │
│   ├── quality_control/             # Quality control app
│   │   ├── api/
│   │   ├── models/
│   │   ├── services/
│   │   ├── templates/
│   │   └── ...
│   │
│   └── dashboard/                   # Dashboard and reporting app
│       ├── api/
│       ├── services/
│       │   ├── __init__.py
│       │   ├── summary_service.py
│       │   └── report_service.py
│       ├── templates/
│       └── ...
│
├── core/                            # Core components shared across apps
│   ├── api/                         # Common API components
│   │   ├── __init__.py
│   │   ├── pagination.py
│   │   ├── permissions.py
│   │   └── throttling.py
│   ├── constants/                   # Project-wide constants
│   │   ├── __init__.py
│   │   ├── choices.py
│   │   └── settings.py
│   ├── middleware/                  # Custom middleware
│   ├── templatetags/                # Custom template tags
│   ├── utils/                       # Utility functions
│   │   ├── __init__.py
│   │   ├── date_utils.py
│   │   ├── file_utils.py
│   │   └── notification_utils.py
│   ├── validators/                  # Custom validators
│   └── mixins/                      # Reusable mixins
│
├── static/                          # Static files
│   ├── css/                         # CSS files (split by functionality)
│   │   ├── base.css
│   │   ├── components/
│   │   │   ├── buttons.css
│   │   │   ├── forms.css
│   │   │   └── ...
│   │   ├── layouts/
│   │   │   ├── dashboard.css
│   │   │   └── ...
│   │   └── pages/
│   │       ├── orders.css
│   │       ├── invoices.css
│   │       └── ...
│   │
│   ├── js/                          # JavaScript files (split by functionality)
│   │   ├── common/
│   │   │   ├── utils.js
│   │   │   └── api.js
│   │   ├── components/
│   │   │   ├── datepicker.js
│   │   │   ├── fileupload.js
│   │   │   └── ...
│   │   └── pages/
│   │       ├── orders/
│   │       │   ├── list.js
│   │       │   ├── detail.js
│   │       │   └── form.js
│   │       ├── invoices/
│   │       └── ...
│   │
│   └── images/
│
├── templates/                       # Global templates
│   ├── base.html                    # Base template
│   ├── partials/                    # Reusable template parts
│   │   ├── header.html
│   │   ├── footer.html
│   │   ├── sidebar.html
│   │   └── ...
│   ├── components/                  # Reusable UI components
│   │   ├── alerts.html
│   │   ├── forms.html
│   │   ├── modals.html
│   │   └── ...
│   ├── layouts/                     # Page layout templates
│   │   ├── dashboard.html
│   │   ├── fullwidth.html
│   │   └── ...
│   └── errors/                      # Error pages
│       ├── 404.html
│       ├── 500.html
│       └── ...
│
├── media/                           # User-uploaded files (not in version control)
│
├── docs/                            # Project documentation
│   ├── api/                         # API documentation
│   ├── development/                 # Development guides
│   └── user/                        # User guides
│
├── scripts/                         # Utility scripts
│   ├── setup.sh
│   └── deploy.sh
│
├── requirements/                    # Pip requirements files
│   ├── base.txt                     # Base requirements
│   ├── development.txt              # Development requirements
│   ├── production.txt               # Production requirements
│   └── test.txt                     # Testing requirements
│
├── manage.py                        # Django management script
├── .env.example                     # Example environment variables
├── .gitignore                       # Git ignore file
├── docker-compose.yml               # Docker Compose configuration
├── Dockerfile                       # Docker configuration
└── README.md                        # Project overview
```

## Modular Coding Guidelines

### 1. Code Organization Principles

#### 1.1 Django Apps Modularization

Each functional domain of the system should be organized as a separate Django app:

- **accounts**: User, role, and team management
- **orders**: Order and component management
- **invoices**: Invoice and payment tracking
- **quality_control**: QC processes and return management
- **dashboard**: Reporting and dashboards

#### 1.2 File Size Limitations

- All Python files should be limited to 500 lines of code
- If a file grows beyond this limit, split it based on logical functionality

### 2. Model Modularization

#### 2.1 Models Organization

For apps with multiple models:

1. Create a `models/` package with `__init__.py` that imports and exposes all models
2. Split models into separate files based on entity (e.g., `order.py`, `component.py`)
3. Keep related models in the same file if their combined size is under 500 lines

Example for orders app:

```python
# apps/orders/models/__init__.py
from .order import Order, OrderStatus, OrderStatusHistory
from .component import Component

__all__ = ['Order', 'OrderStatus', 'OrderStatusHistory', 'Component']
```

```python
# apps/orders/models/order.py
from django.db import models
from django.conf import settings

class Order(models.Model):
    """Order model for tracking procurement requests"""
    # Model fields and methods...

class OrderStatus(models.Model):
    """Status options for orders"""
    # Model fields and methods...

class OrderStatusHistory(models.Model):
    """History of status changes for orders"""
    # Model fields and methods...
```

#### 2.2 Model Methods

- Move complex model methods to service classes when they exceed ~20 lines
- Group related model methods in the model class (e.g., all validation methods together)
- Use abstract base classes for shared model behaviors

### 3. View Modularization

#### 3.1 Class-Based Views

- Use class-based views to avoid code duplication
- Split views into separate files based on functionality
- Organize view mixins in a separate file or in core/mixins

Example structure:

```python
# apps/orders/views/__init__.py
from .order import OrderListView, OrderDetailView, OrderCreateView, OrderUpdateView
from .component import ComponentCreateView, ComponentUpdateView

__all__ = [
    'OrderListView', 'OrderDetailView', 'OrderCreateView', 'OrderUpdateView',
    'ComponentCreateView', 'ComponentUpdateView'
]
```

#### 3.2 API Views

- Organize API views similar to regular views
- Use ViewSets for related CRUD operations
- Split serializers into separate files by entity

### 4. Business Logic Modularization

#### 4.1 Service Layer

Create a service layer for business logic:

```python
# apps/orders/services/order_service.py
class OrderService:
    @staticmethod
    def create_order(data):
        """Create a new order with components"""
        # Business logic for order creation
        
    @staticmethod
    def update_order_status(order, status, user):
        """Update order status with history tracking"""
        # Status update logic
```

#### 4.2 Using Services in Views

```python
# apps/orders/views/order.py
from ..services.order_service import OrderService

class OrderCreateView(CreateView):
    # View configuration
    
    def form_valid(self, form):
        # Use service layer for business logic
        order_data = form.cleaned_data
        order = OrderService.create_order(order_data)
        return redirect(order.get_absolute_url())
```

### 5. Template Modularization

#### 5.1 Template Organization

- Use template inheritance for shared layouts
- Create reusable components in `templates/components/`
- Structure templates to match URL structure

#### 5.2 Template Tags

- Create custom template tags for complex rendering logic
- Organize template tags by functionality

### 6. Static Files Modularization

#### 6.1 CSS Organization

- Use a component-based approach (similar to Tailwind's philosophy)
- Split CSS into base, layout, component, and page-specific files
- Consider using SCSS for better variable and mixin support

#### 6.2 JavaScript Organization

- Split JS by functionality and page/component
- Use ES6 modules for better code organization
- Keep individual JS files focused on single responsibility

Example:

```javascript
// static/js/pages/orders/form.js
import { DatePicker } from '../../components/datepicker.js';
import { FileUpload } from '../../components/fileupload.js';
import { ApiClient } from '../../common/api.js';

// Page-specific functionality
```

### 7. Configuration Modularization

- Split settings.py into multiple files based on environment
- Use environment variables for sensitive configuration
- Create a core/constants package for shared constants

## Coding Standards and Conventions

### 1. Python Code Style

- Follow PEP 8 style guide
- Use consistent naming conventions:
  - Classes: CamelCase
  - Functions/methods: snake_case
  - Constants: UPPER_SNAKE_CASE
- Add docstrings to all classes and methods

### 2. JavaScript Code Style

- Follow a consistent JS style guide (e.g., Airbnb)
- Use ES6+ features
- Implement proper error handling

### 3. Django Model Guidelines

- Define `__str__` methods for all models
- Add Meta classes with proper ordering and verbose names
- Use model managers for query logic
- Define proper related_name for relationships

### 4. Template Standards

- Use template inheritance consistently
- Prefer template includes for reusable components
- Minimize logic in templates

## Importing Guidelines

### 1. Python Import Conventions

- Use absolute imports for clarity
- Group imports in the following order:
  1. Standard library imports
  2. Django framework imports
  3. Third-party library imports
  4. Local application imports
- Sort imports alphabetically within each group

Example:

```python
# Standard library
import datetime
import json

# Django
from django.db import models
from django.urls import reverse

# Third-party
import pytz
from rest_framework import serializers

# Local
from core.utils.date_utils import format_date
from .services.order_service import OrderService
```

### 2. JavaScript Import Conventions

- Use ES6 import syntax
- Group imports similar to Python convention
- Consider using index.js files to simplify imports

## Database Migration Management

- Create focused migrations for specific model changes
- Add descriptive names to migrations
- Document complex migrations

## Testing Structure

- Split tests by test type (unit, integration, functional)
- Create factories for test data using factory_boy
- Use fixtures for complex test setups

## Example: Order Module Implementation

```python
# apps/orders/models/order.py (excerpt)
from django.db import models
from django.conf import settings
from django.urls import reverse

class Order(models.Model):
    ORDER_STATUS_CHOICES = [
        ('requested', 'Order Requested'),
        ('placed', 'Order Placed'),
        ('transit', 'Material in Transit'),
        ('received', 'Material Received'),
        ('qc', 'Material QC'),
        ('handover', 'Material Handover'),
        ('completed', 'Order Completed'),
    ]
    
    order_id = models.CharField(max_length=50, unique=True, editable=False)
    request_id = models.CharField(max_length=50, blank=True, null=True)
    requested_amount = models.DecimalField(max_digits=10, decimal_places=2)
    actual_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    request_person = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='requested_orders'
    )
    request_team = models.ForeignKey(
        'accounts.Team',
        on_delete=models.PROTECT,
        related_name='team_orders'
    )
    current_status = models.CharField(
        max_length=20,
        choices=ORDER_STATUS_CHOICES,
        default='requested'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
    
    def __str__(self):
        return f"Order {self.order_id}"
    
    def get_absolute_url(self):
        return reverse('orders:detail', kwargs={'pk': self.pk})
    
    def is_completed(self):
        return self.current_status == 'completed'
    
    def is_overdue(self):
        # Logic to check if any component is overdue
        pass
```

```python
# apps/orders/models/component.py (excerpt)
from django.db import models

class Component(models.Model):
    order = models.ForeignKey(
        'orders.Order',
        on_delete=models.CASCADE,
        related_name='components'
    )
    name = models.CharField(max_length=255)
    value = models.CharField(max_length=255, blank=True)
    package = models.CharField(max_length=255, blank=True)
    part_number = models.CharField(max_length=255, blank=True)
    quantity = models.PositiveIntegerField()
    links = models.TextField(blank=True)
    due_date = models.DateField()
    comments = models.TextField(blank=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.part_number})"
```

```python
# apps/orders/services/order_service.py (excerpt)
from django.utils import timezone
from django.db import transaction
from ..models import Order, Component, OrderStatusHistory

class OrderService:
    @staticmethod
    def generate_order_id():
        """Generate a unique order ID"""
        prefix = "ORD"
        timestamp = timezone.now().strftime("%Y%m%d%H%M")
        random_suffix = "".join([str(random.randint(0, 9)) for _ in range(4)])
        return f"{prefix}-{timestamp}-{random_suffix}"
    
    @staticmethod
    @transaction.atomic
    def create_order(data, components_data, user):
        """Create a new order with components"""
        # Create order
        order = Order(
            order_id=OrderService.generate_order_id(),
            request_id=data.get('request_id'),
            requested_amount=data.get('requested_amount'),
            request_person=user,
            request_team=data.get('request_team'),
            current_status='requested'
        )
        order.save()
        
        # Create components
        for component_data in components_data:
            Component.objects.create(
                order=order,
                name=component_data.get('name'),
                value=component_data.get('value'),
                package=component_data.get('package'),
                part_number=component_data.get('part_number'),
                quantity=component_data.get('quantity'),
                links=component_data.get('links', ''),
                due_date=component_data.get('due_date'),
                comments=component_data.get('comments', '')
            )
        
        # Create initial status history
        OrderStatusHistory.objects.create(
            order=order,
            status='requested',
            notes="Order created",
            user=user
        )
        
        return order
    
    @staticmethod
    @transaction.atomic
    def update_status(order, new_status, user, notes=''):
        """Update order status with history tracking"""
        if order.current_status != new_status:
            # Update order status
            old_status = order.current_status
            order.current_status = new_status
            order.save(update_fields=['current_status', 'updated_at'])
            
            # Create status history entry
            OrderStatusHistory.objects.create(
                order=order,
                status=new_status,
                previous_status=old_status,
                notes=notes,
                user=user
            )
            
            return True
        return False
```

This modular approach ensures that each file maintains a single responsibility and stays under the 500-line limit while providing a clear organization for the project.

## Conclusion

By following this modular structure, the Inventory Management System will maintain clean, organized code that is easy to maintain and extend. The structure promotes:

1. Separation of concerns
2. Code reusability
3. Maintainability
4. Testability
5. Scalability

This approach aligns with Django best practices while adding additional organization to support a complex application with multiple functional areas. 