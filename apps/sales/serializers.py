from rest_framework import serializers
from products.models import Product
from .models import Sale, SaleItem, SaleEvent
from django.db import transaction
from decimal import Decimal

class SaleItemSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = SaleItem
        fields = [
            'id', 'product', 'unit_price', 'quantity', 'line_total', 
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'line_total']

    def valdate_quantity(self, value):
        if value <=0:
            raise serializers.ValidationError("Quantity must be greater than zero.")      
        return value
    
    def valiadate_unit_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Unit price must be greater than zero.")
        return value
    

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
            raise serializers.ValidationError("A sale must include at least one item.")
        
        return data
    
    def create(self, validated_data):
        request = self.context.get('request')
        items_data = validated_data.pop('items')
        
        if request.user:
            vendor = request.user
        else:
            vendor = validated_data.get('vendor')

        product_ids = [item['product'].id for item in items_data]

        # Atomic transaction - Prevents partially created sales
        with transaction.atomic():
            # Acquire locks on product rows
            products_qs = Product.objects.select_for_update().filter(id__in=product_ids)
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
            sale = Sale.objects.create(vendor=vendor, **validated_data)

            sale_items = []
            total = Decimal('0.00')

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

                prod.quantity -= quantity
                prod.save(update_felds=['quantity'])
                total += line_total

            SaleItem.objects.bulk_create(sale_items)
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