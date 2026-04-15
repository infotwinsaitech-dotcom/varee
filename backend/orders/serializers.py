from rest_framework import serializers
from .models import Order
from backend.products.serializers import ProductSerializer


class OrderSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    product_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Order
        fields = ['id', 'product', 'product_id', 'quantity', 'status', 'total_price']

    def create(self, validated_data):
        product_id = validated_data.pop('product_id')
        user = self.context['request'].user

        from backend.products.models import Product
        product = Product.objects.get(id=product_id)

        order = Order.objects.create(
            product=product,
            quantity=validated_data['quantity'],
            user=user
        )
        return order