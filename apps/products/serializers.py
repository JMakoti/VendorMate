from rest_framework import serializers
from .models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'category', 'name', 'slug', 'description', 'price', 'stock', 'image', 'is_available', 'created_at', 'updated_at']
    
    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than zero")
        return value
    
    def validate_stock(self, value):
        if value < 0:
            raise serializers.ValidationError("Stock cannot be negative")
        return value
    
class ProductStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["stock"]

    def validate_stock(self, value):
        if not isinstance(value, int) or value < 0:
            raise serializers.ValidationError("Stock must be a non-negative integer.")
        return value
