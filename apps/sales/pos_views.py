from django.db import transaction
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema
from drf_spectacular.types import OpenApiTypes
from decimal import Decimal

from apps.products.models import Product
from .models import Sale, SaleItem, SaleEvent
from .serializers import SaleSerializer

@extend_schema(
    summary="Quick POS Sale",
    description="Create a sale quickly for POS operations with automatic calculations",
    request=OpenApiTypes.OBJECT,
    responses={201: SaleSerializer, 400: OpenApiTypes.OBJECT}
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def pos_quick_sale(request):
    """Quick sale creation for POS operations"""
    items = request.data.get('items', [])
    customer_payment = Decimal(str(request.data.get('payment_amount', 0)))
    payment_method = request.data.get('payment_method', 'CASH')
    
    if not items:
        return Response({'error': 'Items are required'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        with transaction.atomic():
            # Create sale
            sale = Sale.objects.create(vendor=request.user)
            
            total_amount = Decimal('0.00')
            sale_items = []
            
            # Process each item
            for item_data in items:
                product_id = item_data.get('product_id')
                quantity = int(item_data.get('quantity', 1))
                
                try:
                    product = Product.objects.select_for_update().get(id=product_id)
                except Product.DoesNotExist:
                    return Response({'error': f'Product {product_id} not found'}, 
                                  status=status.HTTP_400_BAD_REQUEST)
                
                # Check stock
                if product.stock < quantity:
                    return Response({'error': f'Insufficient stock for {product.name}'}, 
                                  status=status.HTTP_400_BAD_REQUEST)
                
                # Calculate prices
                unit_price = product.price
                line_total = unit_price * quantity
                
                # Create sale item
                sale_item = SaleItem.objects.create(
                    sale=sale,
                    product=product,
                    quantity=quantity,
                    unit_price=unit_price,
                    line_total=line_total
                )
                
                # Update stock
                product.stock -= quantity
                product.save()
                
                total_amount += line_total
                sale_items.append(sale_item)
            
            # Update sale total
            sale.total_amount = total_amount
            
            # Handle payment
            if customer_payment >= total_amount:
                sale.status = 'COMPLETED'
                sale.payment_reference = f'POS-{sale.id}-{payment_method}'
                
                # Log payment event
                SaleEvent.objects.create(
                    sale=sale,
                    actor=request.user,
                    event_type='MARKED_PAID',
                    payload={
                        'payment_method': payment_method,
                        'amount_paid': str(customer_payment),
                        'change': str(customer_payment - total_amount)
                    }
                )
            
            sale.save()
            
            # Prepare response
            change = customer_payment - total_amount if customer_payment >= total_amount else Decimal('0.00')
            
            return Response({
                'sale_id': sale.id,
                'total_amount': total_amount,
                'payment_received': customer_payment,
                'change': change,
                'status': sale.status,
                'items': len(sale_items),
                'receipt_number': f'RCP-{sale.id:06d}'
            }, status=status.HTTP_201_CREATED)
            
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@extend_schema(
    summary="Get POS receipt",
    description="Get formatted receipt data for printing",
    responses={200: OpenApiTypes.OBJECT}
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def pos_receipt(request, sale_id):
    """Get receipt data for POS printing"""
    try:
        sale = Sale.objects.select_related('vendor').prefetch_related(
            'items__product'
        ).get(id=sale_id, vendor=request.user)
        
        receipt_data = {
            'receipt_number': f'RCP-{sale.id:06d}',
            'date': sale.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'vendor': sale.vendor.username,
            'items': [],
            'subtotal': sale.total_amount,
            'total': sale.total_amount,
            'status': sale.status
        }
        
        for item in sale.items.all():
            receipt_data['items'].append({
                'name': item.product.name,
                'quantity': item.quantity,
                'unit_price': item.unit_price,
                'line_total': item.line_total
            })
        
        return Response(receipt_data, status=status.HTTP_200_OK)
        
    except Sale.DoesNotExist:
        return Response({'error': 'Sale not found'}, status=status.HTTP_404_NOT_FOUND)

@extend_schema(
    summary="Search products for POS",
    description="Search products by name or barcode for POS operations",
    responses={200: OpenApiTypes.OBJECT}
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def pos_product_search(request):
    """Search products for POS"""
    query = request.GET.get('q', '').strip()
    
    if not query:
        return Response({'error': 'Search query required'}, status=status.HTTP_400_BAD_REQUEST)
    
    products = Product.objects.filter(
        name__icontains=query,
        is_available=True
    ).values('id', 'name', 'price', 'stock')[:20]
    
    return Response(list(products), status=status.HTTP_200_OK)