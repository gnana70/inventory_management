"""
URL configuration for inventory_management project.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    # Include app-specific URLs
    path('accounts/', include('apps.accounts.urls')),
    path('orders/', include('apps.orders.urls')),
    path('invoices/', include('apps.invoices.urls')),  # Invoice management app
    path('quality-control/', include('apps.quality_control.urls')),
    path('dashboard/', include('apps.dashboard.urls')),
    # Set the root URL to redirect to dashboard
    path('', RedirectView.as_view(url='/dashboard/'), name='home'),
]

# Add debug toolbar URLs in development
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
    # Serve media files in development
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 