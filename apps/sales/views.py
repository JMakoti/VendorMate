from django.shortcuts import render
from django.db import transaction
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Sale
from .serializers import SaleSerializer


class SaleViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.all().prefetch_related('items__product')
    serializer = SaleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return self.queryset
        
        return self.queryset.filter(vendor=user)
    
    def perform_create(self, serializer):
        serializer.save(vendor=self.request.user)

    @action(detail=True, methods=['post'], url_path='mark-paid')
    def mark_paid(self, request, pk=None):
        """Mark a sale as paid. To be called by Payments app."""
        sale = self.get_object()
        if sale.status == 'COMPLETED':
            return Response({'detail': 'Sale already completed.'}, status=status.HTTP_200_OK)
        
        payment_reference = request.data.get('payment_reference')
        amount = Decimal(request.data.get('amount', '0.00'))

        # Ensure amount paid matches the total balance due
        if amount != sale.total_amount:
            return Response(
                {'detail': 'Amount does not match the sale total.'}, 
                status=status.HTTP_400_BAD_REQUEST
        )

        # Prevent double writing of the same payment reference
        if payment_reference and sale.payment_reference == payment_reference:
            return Response({'detail': 'Payment already recorded.'})
        
        # Update sale
        sale.payment_reference = payment_reference
        sale.status = 'COMPLETED'
        sale.save(update_fields=['payment_reference', 'status', 'updated_at'])

        # Record sale paid event
        SaleEvent.objects.create(
            sale=sale, 
            event_type='MARKED_PAID', 
            payload={'payload': request.data}, 
            actor=None
        )

        return Response({'detail': 'Sale marked as completed.'}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'], url_path='cancel')
    def cancel(self, request, pk=None):
        """Cancel a sale."""
        sale = self.get_object()
        if sale.status != 'PENDING':
            return Response(
                {'detail': 'Only pending sales can be cancelled.'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Restore stock
        with transaction.atomic():
            for item in sale.items.select_related('product').all():
                prod = item.product
                prod.stock = prod.stock + item.quantity
                prod.save(update_fields=['stock'])

            sale.status = 'CANCELLED'
            sale.save(update_fields=['status'])

            # Record sale cancellation event
            SaleEvent.objects.create(
                sale=sale, 
                event_type='CANCELLED', 
                payload={'reason': request.data.get('reason')}, 
                actor=request.user
            )

        return Response({'detail': 'Sale cancelled and stock restored.'}, status=status.HTTP_200_OK)