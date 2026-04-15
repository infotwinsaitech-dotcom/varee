from rest_framework.decorators import api_view
from rest_framework.response import Response
from backend.products.models import Product
from backend.orders.models import Order
from django.contrib.auth.models import User

@api_view(['GET'])
def dashboard_api(request):
    products = Product.objects.count()
    orders = Order.objects.count()
    users = User.objects.count()

    revenue = sum([o.total_price for o in Order.objects.all()])

    return Response({
        "products": products,
        "orders": orders,
        "users": users,
        "revenue": revenue
    })