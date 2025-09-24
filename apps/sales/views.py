from django.db import transaction
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view
from .models import Sale
from .serializers import SaleSerializer, MarkPaidSerializer, CancelSaleSerializer
from .services import mark_sale_as_paid, cancel_sale


@extend_schema_view(
    list=extend_schema(
        summary="List sales",
        description="Retrieve a list of sales for the authenticated user"
    ),
    create=extend_schema(
        summary="Create sale",
        description="Create a new sale with items"
    ),
    retrieve=extend_schema(
        summary="Get sale details",
        description="Retrieve details of a specific sale"
    ),
    update=extend_schema(
        summary="Update sale",
        description="Update an existing sale"
    ),
    partial_update=extend_schema(
        summary="Partially update sale",
        description="Partially update an existing sale"
    ),
    destroy=extend_schema(
        summary="Delete sale",
        description="Delete an existing sale"
    )
)
class SaleViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.all().prefetch_related('items__product')
    serializer_class = SaleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return self.queryset
        
        return self.queryset.filter(vendor=user)
    
    def perform_create(self, serializer):
        serializer.save(vendor=self.request.user)

    @extend_schema(
        summary="Mark sale as paid",
        description="Mark a sale as paid with payment reference",
        request=MarkPaidSerializer
    )
    @action(detail=True, methods=['post'], url_path='mark-paid')
    def mark_paid(self, request, pk=None):
        """Mark a sale as paid."""
        sale = self.get_object()
        serializer = MarkPaidSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        amount = serializer.validated_data.get('amount')

        # Ensure amount paid matches the total balance due
        if amount != sale.total_amount:
            return Response(
                {'detail': 'Amount does not match the sale total.'}, 
                status=status.HTTP_400_BAD_REQUEST
        )

        # Call the service layer with a lock
        with transaction.atomic():
            sale, response_data, response_status = mark_sale_as_paid(
                sale=sale,
                payment_reference=serializer.validated_data.get('payment_reference'),
                actor=request.user
            )

        return Response(response_data, status=response_status)
    
    @extend_schema(
        summary="Cancel sale",
        description="Cancel a sale and restore product stock",
        request=CancelSaleSerializer
    )
    @action(detail=True, methods=['post'], url_path='cancel')
    def cancel(self, request, pk=None):
        """Cancel a sale and restore product stock."""
        sale = self.get_object()
        serializer = CancelSaleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        sale, response_data, response_status = cancel_sale(
            sale=sale,
            actor=request.user,
            reason=serializer.validated_data.get('reason')
        )


        return Response({'detail': 'Sale cancelled and stock restored.'}, status=status.HTTP_200_OK)