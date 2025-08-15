from django.db import transaction
from .models import Sale, SaleEvent
from apps.products.models import Products


def mark_sale_as_paid(sale, payment_reference, actor):
    """Marks a sale as paid."""
    sale = Sale.objects.select_for_update().get(pk=sale.pk)

    if sale.status == 'COMPLETED':
        return sale, {'detail': 'Sale already completed.'}, 200

    # Ensure a payment reference is provided for updates
    if not payment_reference:
        return sale, {'detail': 'Payment reference is required.'}, 400

    # Prevent double writing of the same payment reference
    if sale.payment_reference == payment_reference:
        return sale, {'detail': 'Payment already recorded.'}, 200

    sale.payment_reference = payment_reference
    sale.status = 'COMPLETED'
    sale.save(update_fields=['payment_reference', 'status', 'updated_at'])

    SaleEvent.objects.create(
        sale=sale,
        event_type='MARKED_PAID',
        payload={'payment_reference': payment_reference},
        actor=actor
    )

    return sale, {'detail': 'Sale is marked as completed.'}, 200


def cancel_sale(sale, actor, reason=None):
    """Marks a sale as cancelled."""
    if sale.status != 'PENDING':
        return sale, {'detail': 'Only pending sales can be cancelled'}

    with transaction.atomic():
        sale_items = sale.items.select_related('product').all()
        products_to_update = []

        for item in sale_items:
            prod = item.product
            prod.stock += item.quantity
            products_to_update.append(prod)

        Products.objects.bulk_update(products_to_update, ['stock'])

        sale.status = 'CANCELLED'
        sale.save(updated_fields=['status'])

        SaleEvent.objects.create(
            sale=sale,
            event_type='CANCELLED',
            payload={'reason': reason},
            actor=actor
        )

    return sale, {'detail': 'Sale cancelled and stock restored.'}, 200
