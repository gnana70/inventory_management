# Generated by Django 4.2.20 on 2025-04-07 12:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(editable=False, max_length=50, unique=True, verbose_name='Order ID')),
                ('request_id', models.CharField(blank=True, max_length=50, null=True, verbose_name='Request ID')),
                ('requested_amount', models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name='Requested Amount')),
                ('actual_amount', models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name='Actual Amount')),
                ('status', models.CharField(choices=[('requested', 'Order Requested'), ('placed', 'Order Placed'), ('in_transit', 'Material in Transit'), ('received', 'Material Received'), ('qc', 'Material QC'), ('handover', 'Material Handover'), ('completed', 'Order Completed')], default='requested', max_length=20, verbose_name='Status')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated At')),
                ('completed_at', models.DateTimeField(blank=True, null=True, verbose_name='Completed At')),
                ('notes', models.TextField(blank=True, verbose_name='Notes')),
                ('request_person', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='requested_orders', to=settings.AUTH_USER_MODEL, verbose_name='Request Person')),
                ('requested_team', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='team_orders', to='accounts.team', verbose_name='Requested Team')),
            ],
            options={
                'verbose_name': 'Order',
                'verbose_name_plural': 'Orders',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='OrderStatusHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('requested', 'Order Requested'), ('placed', 'Order Placed'), ('in_transit', 'Material in Transit'), ('received', 'Material Received'), ('qc', 'Material QC'), ('handover', 'Material Handover'), ('completed', 'Order Completed')], max_length=20, verbose_name='Status')),
                ('changed_at', models.DateTimeField(auto_now_add=True, verbose_name='Changed At')),
                ('notes', models.TextField(blank=True, verbose_name='Notes')),
                ('changed_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='status_changes', to=settings.AUTH_USER_MODEL, verbose_name='Changed By')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='status_history', to='orders.order', verbose_name='Order')),
            ],
            options={
                'verbose_name': 'Order Status History',
                'verbose_name_plural': 'Order Status History',
                'ordering': ['-changed_at'],
            },
        ),
        migrations.CreateModel(
            name='Component',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('value', models.CharField(blank=True, max_length=255, verbose_name='Value')),
                ('package', models.CharField(blank=True, max_length=255, verbose_name='Package')),
                ('part_number', models.CharField(blank=True, max_length=255, verbose_name='Part Number')),
                ('quantity', models.PositiveIntegerField(default=1, verbose_name='Quantity')),
                ('links', models.TextField(blank=True, verbose_name='Links')),
                ('due_date', models.DateField(blank=True, null=True, verbose_name='Due Date')),
                ('comments', models.TextField(blank=True, verbose_name='Comments')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated At')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='components', to='orders.order', verbose_name='Order')),
            ],
            options={
                'verbose_name': 'Component',
                'verbose_name_plural': 'Components',
                'ordering': ['name'],
            },
        ),
    ]
