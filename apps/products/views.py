from django.shortcuts import render
from .models import Category , Products
from .serializers import CategorySerializer, ProductSerializer ,ProductStockSerializer
from rest_framework import generics, status
from rest_framework.response import Response

# Category views
class ListCategory(generics.ListAPIView):
    """List All Available Categories"""

    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    
    def list(self, request ,*args, **kwargs):
        """Overide List Method & & Customize Listing Response"""
        try:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset,many= True)

            return Response({
                "message":"All categories Listing successfuly",
                "count":queryset.count(),
                "data":serializer.data,
            },
            status=status.HTTP_200_OK,)
        except Exception as e:
            """Catch & Return an Error"""
            return Response(
                {
                    "message":"An Error Ocuurred While Listing the categories",
                    "error":str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

class CreateCategory(generics.CreateAPIView):
    """Creating A New Category"""
    serializer_class = CategorySerializer

    def create(self, request , *args ,**kwargs):
        """Overide Create Method & Customize the Create response"""

        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)

            return Response({
                "message": f'Category {serializer.instance.name} has been created successfully',
                "data": serializer.data,
            },
            status=status.HTTP_201_CREATED,)
        
        except Exception as e:
            """Catch & Return an Error"""
            return Response(
                {
                    "message":"An Error Ocuurred While Creating a new category",
                    "error":str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
    
class UpdateCategory(generics.UpdateAPIView):
    """Update An Existing Category By ID"""

    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    lookup_field = "pk"

    def update(self ,request ,*args ,**kwargs):
        """Overide Update Method & Customize the Update Response"""
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
                    "message":f'Category {serializer.instance.name} has been updated successfully',
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {
                    "message": "An error occurred while updating the Category",
                    "error": str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

class DeleteCategory(generics.DestroyAPIView):
    """Delete An Existing Category by ID """

    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    lookup_field = "pk"

    def destroy(self, request, *args, **kwargs):
        """Overide Delete Method & Customize Response"""
        try:
            instance = self.get_object()
            instance.delete()
            return Response({
                "Message":f'Category {instance.name} has been deleted successfully',
            },
            status=status.HTTP_200_OK,)
        except Exception as e:
            return Response({
                "Message":"Error Occured While Deleting The Category",
                "error":str(e)
            })


# Product views
class ListProduct(generics.ListAPIView):
    """Listing the Products"""
    serializer_class = ProductSerializer
    queryset = Products.objects.all()
    
    def list(self, request ,*args, **kwargs):
        """Overide List Method & & Customize Listing Response"""
        try:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset,many= True)

            return Response({
                "message":"All Products Listing successfuly",
                "count":queryset.count(),
                "data":serializer.data,
            },
            status=status.HTTP_200_OK,)
        except Exception as e:
            """Catch & Return an Error"""
            return Response(
                {
                    "message":"An Error Ocuurred While Listing the Products",
                    "error":str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
class CreateProduct(generics.CreateAPIView):
        """Creating A New Product"""
        serializer_class = ProductSerializer

        def create(self, request , *args ,**kwargs):
            """Overide Create Method & Customize the Create response"""

            try:
                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                self.perform_create(serializer)

                return Response({
                    "message":f'Product {serializer.instance.name} has been created successfully',
                    "data":serializer.data,
                },
                status=status.HTTP_201_CREATED,)
            
            except Exception as e:
                """Catch & Return an Error"""
                return Response(
                    {
                        "message":"An Error Ocuurred While Creating a new Product",
                        "error":str(e)
                    },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
class ProductDetail(generics.RetrieveAPIView):
    """
    Retrieve a specific product by ID.
    """

    serializer_class = ProductSerializer
    queryset = Products.objects.all()
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
                    "message": f'Product {instance.name} has been retrived successfully',
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            """Catch & Return an Error"""
            return Response(
                {
                    "message": "An error occurred while retrieving the product",
                    "error": str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
class UpdateProduct(generics.UpdateAPIView):
    """Update An Existing Product By ID"""

    serializer_class = ProductSerializer
    queryset = Products.objects.all()
    lookup_field = "pk"

    def update(self ,request ,*args ,**kwargs):
        """Overide Update Method & Customize the Update Response"""
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
                    "message":f'Product {serializer.instance.name} has been updated successfully',
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {
                    "message": "An error occurred while updating the Category",
                    "error": str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
class DeleteProduct(generics.DestroyAPIView):
    """Delete An Existing Product by ID """

    serializer_class = ProductSerializer
    queryset = Products.objects.all()
    lookup_field = "pk"

    def destroy(self, request, *args, **kwargs):
        """Overide Delete Method & Customize Response"""
        try:
            instance = self.get_object()
            instance.delete()
            return Response({
                "Message":f'Product {instance.name} has been deleted successfully',
            },
            status=status.HTTP_200_OK,)
        except Exception as e:
            return Response({
                "Message":"Error Occured While Deleting The Product",
                "error":str(e)
            })

class UpdateProductStock(generics.UpdateAPIView):
    """Update only the stock of a product"""

    serializer_class = ProductStockSerializer
    queryset = Products.objects.all()
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
                    "message": f'Product {instance.name} stock updated successfully',
                    "new_stock": instance.stock,
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response(
                {"message": "Error occurred while updating stock", "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
