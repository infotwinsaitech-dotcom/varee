from rest_framework import serializers
from .models import CartItem

class CartSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_price = serializers.IntegerField(source='product.price', read_only=True)
    product_image = serializers.ImageField(source='product.image', read_only=True)
    product_category = serializers.CharField(source='product.category.name', read_only=True)

    class Meta:
        model = CartItem
        fields = [
            'id',
            'product',
            'quantity',
            'product_name',
            'product_price',
            'product_image',
            'product_category'
        ]