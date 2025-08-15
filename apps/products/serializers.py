from rest_framework import serializers
from .models import Category , Products


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = "__all__"

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be a positive integer.")
        return value
    
class ProductStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ["stock"]

    def validate_stock(self, value):
        if not isinstance(value, int) or value < 0:
            raise serializers.ValidationError("Stock must be a non-negative integer.")
        return value
