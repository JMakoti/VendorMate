from decimal import Decimal
from django.db import models
from django.conf import settings

class Sale(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'), 
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]
    
    vendor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default='PENDING')
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    payment_reference = models.CharField(max_length=255, null=True, blank=True, unique=True)
    notes = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(total_amount__gte=Decimal('0.00')),
                name='check_sale_total_amount_non_negative',
            )
        ]

    def __str__(self):
        return f"Sale {self.id} ({self.status})"


class SaleItem(models.Model):
    sale = models.ForeignKey('sales.Sale', on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('products.Products', on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    line_total = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal('0.00'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        constraints = [
            models.CheckConstraint(            
                check=models.Q(unit_price__gte=Decimal('0.00')),
                name='check_sale_item_unit_price_non_negative',
            ),
            models.CheckConstraint(
                check=models.Q(line_total__gte=Decimal('0.00')),
                name='check_sale_item_line_total_non_negative',
            ),
            models.UniqueConstraint(
                fields=['sale', 'product'],
                name='unique_sale_product_per_sale'
            )
        ]

    def __str__(self):
        return f"{self.quantity} x {self.product.name} @ {self.unit_price}"


class SaleEvent(models.Model):
    EVENT_TYPE_CHOICES = [
        ('CREATED', 'Created'), 
        ('CANCELLED', 'Cancelled'), 
        ('MARKED_PAID', 'Marked Paid')
    ]

    sale = models.ForeignKey('sales.Sale', on_delete=models.CASCADE)
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    event_type = models.CharField(max_length=32, choices=EVENT_TYPE_CHOICES)
    payload = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Event for Sale {self.sale.id}: {self.event_type}"
