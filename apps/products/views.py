from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ValidationError
from django.http import Http404
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer, ProductStockSerializer
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.serializers import ValidationError as DRFValidationError
from drf_spectacular.utils import extend_schema, extend_schema_view
import html

# Category views
@extend_schema_view(
    get=extend_schema(
        summary="List all categories",
        description="Retrieve a list of all product categories"
    )
)
class ListCategory(generics.ListAPIView):
    """List All Available Categories"""

    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    # permission_classes = IsAuthenticated
    
    def list(self, request, *args, **kwargs):
        """Override List Method & Customize Listing Response"""
        try:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)

            return Response({
                "message": "All categories listing successfully",
                "count": queryset.count(),
                "data": serializer.data,
            }, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response(
                {
                    "message": "Validation error occurred while listing categories",
                    "error": html.escape(str(e))
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response(
                {
                    "message": "An error occurred while listing the categories",
                    "error": html.escape(str(e))
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

@extend_schema_view(
    post=extend_schema(
        summary="Create category",
        description="Create a new product category"
    )
)
class CreateCategory(generics.CreateAPIView):
    """Creating A New Category"""
    serializer_class = CategorySerializer

    def create(self, request, *args, **kwargs):
        """Override Create Method & Customize the Create response"""

        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)

            return Response({
                "message": f'Category {html.escape(serializer.instance.name)} has been created successfully',
                "data": serializer.data,
            }, status=status.HTTP_201_CREATED)
        
        except DRFValidationError as e:
            return Response(
                {
                    "message": "Validation error occurred while creating category",
                    "error": html.escape(str(e))
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response(
                {
                    "message": "An error occurred while creating a new category",
                    "error": html.escape(str(e))
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
    
@extend_schema_view(
    put=extend_schema(
        summary="Update category",
        description="Update an existing category"
    ),
    patch=extend_schema(
        summary="Partially update category",
        description="Partially update an existing category"
    )
)
class UpdateCategory(generics.UpdateAPIView):
    """Update An Existing Category By ID"""

    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    lookup_field = "pk"

    def update(self, request, *args, **kwargs):
        """Override Update Method & Customize the Update Response"""
        try:
            partial = kwargs.pop("partial", False)
            instance = self.get_object()
            serializer = self.get_serializer(
                instance, data=request.data, partial=partial
            )
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

            return Response(
                {
                    "message": f'Category {html.escape(serializer.instance.name)} has been updated successfully',
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        except Http404:
            return Response(
                {
                    "message": "Category not found"
                },
                status=status.HTTP_404_NOT_FOUND,
            )
        except DRFValidationError as e:
            return Response(
                {
                    "message": "Validation error occurred while updating category",
                    "error": html.escape(str(e))
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response(
                {
                    "message": "An error occurred while updating the category",
                    "error": html.escape(str(e))
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

@extend_schema_view(
    delete=extend_schema(
        summary="Delete category",
        description="Delete an existing category"
    )
)
class DeleteCategory(generics.DestroyAPIView):
    """Delete An Existing Category by ID """

    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    lookup_field = "pk"

    def destroy(self, request, *args, **kwargs):
        """Override Delete Method & Customize Response"""
        try:
            instance = self.get_object()
            instance.delete()
            return Response({
                "message": f'Category {html.escape(instance.name)} has been deleted successfully',
            }, status=status.HTTP_200_OK)
        except Http404:
            return Response({
                "message": "Category not found"
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                "message": "Error occurred while deleting the category",
                "error": html.escape(str(e))
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Product views
@extend_schema_view(
    get=extend_schema(
        summary="List all products",
        description="Retrieve a list of all products"
    )
)
class ListProduct(generics.ListAPIView):
    """Listing the Products"""
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    
    def list(self, request, *args, **kwargs):
        """Override List Method & Customize Listing Response"""
        try:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)

            return Response({
                "message": "All products listing successfully",
                "count": queryset.count(),
                "data": serializer.data,
            }, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response(
                {
                    "message": "Validation error occurred while listing products",
                    "error": html.escape(str(e))
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response(
                {
                    "message": "An error occurred while listing the products",
                    "error": html.escape(str(e))
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
@extend_schema_view(
    post=extend_schema(
        summary="Create product",
        description="Create a new product"
    )
)
class CreateProduct(generics.CreateAPIView):
    """Creating A New Product"""
    serializer_class = ProductSerializer

    def create(self, request, *args, **kwargs):
        """Override Create Method & Customize the Create response"""

        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)

            return Response({
                "message": f'Product {html.escape(serializer.instance.name)} has been created successfully',
                "data": serializer.data,
            }, status=status.HTTP_201_CREATED)
        
        except DRFValidationError as e:
            return Response(
                {
                    "message": "Validation error occurred while creating product",
                    "error": html.escape(str(e))
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response(
                {
                    "message": "An error occurred while creating a new product",
                    "error": html.escape(str(e))
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
@extend_schema_view(
    get=extend_schema(
        summary="Get product details",
        description="Retrieve details of a specific product"
    )
)
class ProductDetail(generics.RetrieveAPIView):
    """
    Retrieve a specific product by ID.
    """

    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    lookup_field = "pk"

    def retrieve(self, request, *args, **kwargs):
        """
        Override the retrieve method to return a custom response.
        """
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)

            return Response(
                {
                    "message": f'Product {html.escape(instance.name)} has been retrieved successfully',
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        except Http404:
            return Response(
                {
                    "message": "Product not found"
                },
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            return Response(
                {
                    "message": "An error occurred while retrieving the product",
                    "error": html.escape(str(e))
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
@extend_schema_view(
    put=extend_schema(
        summary="Update product",
        description="Update an existing product"
    ),
    patch=extend_schema(
        summary="Partially update product",
        description="Partially update an existing product"
    )
)
class UpdateProduct(generics.UpdateAPIView):
    """Update An Existing Product By ID"""

    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    lookup_field = "pk"

    def update(self, request, *args, **kwargs):
        """Override Update Method & Customize the Update Response"""
        try:
            partial = kwargs.pop("partial", False)
            instance = self.get_object()
            serializer = self.get_serializer(
                instance, data=request.data, partial=partial
            )
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(
                {
                    "message": f'Product {html.escape(serializer.instance.name)} has been updated successfully',
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        except Http404:
            return Response(
                {
                    "message": "Product not found"
                },
                status=status.HTTP_404_NOT_FOUND,
            )
        except DRFValidationError as e:
            return Response(
                {
                    "message": "Validation error occurred while updating product",
                    "error": html.escape(str(e))
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response(
                {
                    "message": "An error occurred while updating the product",
                    "error": html.escape(str(e))
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
@extend_schema_view(
    delete=extend_schema(
        summary="Delete product",
        description="Delete an existing product"
    )
)
class DeleteProduct(generics.DestroyAPIView):
    """Delete An Existing Product by ID """

    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    lookup_field = "pk"

    def destroy(self, request, *args, **kwargs):
        """Override Delete Method & Customize Response"""
        try:
            instance = self.get_object()
            instance.delete()
            return Response({
                "message": f'Product {html.escape(instance.name)} has been deleted successfully',
            }, status=status.HTTP_200_OK)
        except Http404:
            return Response({
                "message": "Product not found"
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                "message": "Error occurred while deleting the product",
                "error": html.escape(str(e))
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@extend_schema_view(
    # put=extend_schema(
    #     summary="Update product stock",
    #     description="Update stock quantity for a product"
    # ),
    patch=extend_schema(
        summary="Update product stock",
        description="Update stock quantity for a product"
    )
)
class UpdateProductStock(generics.UpdateAPIView):
    """Update only the stock of a product"""

    serializer_class = ProductStockSerializer
    queryset = Product.objects.all()
    lookup_field = "pk"

    def update(self, request, *args, **kwargs):
        try:
            partial = kwargs.pop("partial", False)
            instance = self.get_object()
            serializer = self.get_serializer(
                instance, data=request.data, partial=partial
            )
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(
                {
                    "message": f'Product {html.escape(instance.name)} stock updated successfully',
                    "new_stock": instance.stock,
                },
                status=status.HTTP_200_OK,
            )
        except Http404:
            return Response(
                {"message": "Product not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except DRFValidationError as e:
            return Response(
                {"message": "Validation error occurred while updating stock", "error": html.escape(str(e))},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response(
                {"message": "Error occurred while updating stock", "error": html.escape(str(e))},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
