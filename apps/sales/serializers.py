from rest_framework import serializers
from apps.products.models import Products
from .models import Sale, SaleItem, SaleEvent
from django.db import transaction
from decimal import Decimal

class SaleItemSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Products.objects.all())

    class Meta:
        model = SaleItem
        fields = [
            'id', 'product', 'quantity', 'unit_price', 'line_total',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'line_total']

    def validate(self, data):
        unit_price = data.get('unit_price')
        quantity = data.get('quantity')

        if quantity is not None and quantity <= 0:
            raise serializers.ValidationError({'quantity': 'Quantity must be greater than zero.'})

        if unit_price is not None and unit_price < Decimal('0.00'):
            raise serializers.ValidationError({'unit_price': 'Unit price cannot be negative.'})

    def create(self, validated_data):
        unit_price = validated_data.get('unit_price')
        quantity = validated_data.get('quantity')
        validated_data.update({'line_total': unit_price * quantity})
        return self.Meta.model.objects.create(**validated_data)


class SaleSerializer(serializers.ModelSerializer):
    items = SaleItemSerializer(many=True)
    vendor = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = Sale
        fields = [
            'id', 'vendor', 'status', 'payment_reference', 'notes', 
            'total_amount', 'items', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'total_amount', 'status', 'created_at']

    def validate(self, data):
        items = data.get('items', [])
        if not items:
            raise serializers.ValidationError({"items": "A sale must include at least one item."})
        
        return data
    
    def create(self, validated_data):
        items_data = validated_data.pop('items')
        vendor = validated_data.pop('vendor')
        product_ids = [item['product'].id for item in items_data]

        # Atomic transaction - Prevents partially created sales
        with transaction.atomic():
            # Acquire locks on product rows
            products_qs = Products.objects.select_for_update().filter(id__in=product_ids)
            products_map = {prod.id: prod for prod in products_qs}

            # Stock validation
            for it in items_data:
                prod = products_map.get(it['product'].id)
                if not prod:
                    raise serializers.ValidationError(f"Product {it['product'].id} not found.")
                if prod.stock < it['quantity']:
                    raise serializers.ValidationError(
                        f"Insufficient stock for product {prod.id} ({prod.quantity} available)."
                    )

            # Create sale
            sale = Sale.objects.create(**validated_data)

            sale_items = []
            total = Decimal('0.00')
            products_to_update = []

            # Create sales items
            for it in items_data:
                prod = products_map[it['product'].id]
                unit_price = Decimal(it.get('unit_price', prod.price))
                quantity = int(it['quantity'])
                line_total = unit_price * quantity

                sale_item = SaleItem(
                    sale=sale,
                    product=prod,
                    unit_price=unit_price,
                    quantity=quantity,
                    line_total=line_total
                )
                sale_items.append(sale_item)

                prod.stock -= quantity
                products_to_update.append(prod)
                total += line_total

            SaleItem.objects.bulk_create(sale_items)
            Products.objects.bulk_update(products_to_update, ['stock'])
            sale.total_amount = total
            sale.save(update_fields=['total_amount'])

            # Record sales event
            SaleEvent.objects.create(
                sale=sale,
                event_type='CREATED',
                payload={'total': str(total)},
                actor=vendor
            )

            return sale
        

class MarkPaidSerializer(serializers.Serializer):
    payment_reference = serializers.CharField(required=True, max_length=255)
    amount = serializers.DecimalField(max_digits=12, decimal_places=2, required=True)


class CancelSaleSerializer(serializers.Serializer):
    reason = serializers.CharField(required=False, max_length=255)
    