import hashlib
import hmac
import razorpay

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


from backend.cart.models import Cart
from .models import Order, OrderItem

client = razorpay.Client(auth=("rzp_test_SctBLJdpZLfuV2", "s5imSJzeEbJAXBYjEK0ufmng"))

# ===============================
# COMMON USER
# ===============================
def get_user(request):
    if request.user.is_authenticated:
        return request.user

    user, _ = User.objects.get_or_create(username="guest_user")
    return user

# ===============================
# GET ORDERS
# ===============================
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_orders(request):

    user = get_user(request)

    orders = Order.objects.filter(user=user).order_by('-id')

    data = []

    for order in orders:
        items = OrderItem.objects.filter(order=order)

        order_items = []
        for item in items:
            order_items.append({
                "product_name": item.product.name,
                "quantity": item.quantity,
                "price": item.price,
                "product_image": item.product.image.url if item.product.image else ""
            })

        data.append({
            "id": order.id,
            "total_price": order.total_price,
            "address": order.address,
            "payment_method": order.payment_method,
            "status": order.status,
            "created_at": order.created_at,
            "items": order_items
        })

    return Response(data)

# ===============================
# PLACE ORDER (🔥 FIXED)
# ===============================
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def place_order(request):

    user = get_user(request)   # ✅ IMPORTANT CHANGE

    address = request.data.get("address")
    payment_method = request.data.get("payment_method")

    if not address:
        return Response({"error": "Address is required"}, status=400)

    if not payment_method:
        return Response({"error": "Payment method required"}, status=400)

    cart_items = Cart.objects.filter(user=user)

    if not cart_items.exists():
        return Response({"error": "Cart is empty"}, status=400)

    total = sum(item.product.price * item.quantity for item in cart_items)

    order = Order.objects.create(
        user=user,
        address=address,
        payment_method=payment_method,
        total_price=total
    )

    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price
        )

    cart_items.delete()

    return Response({"message": "Order placed successfully"})

# ===============================
# CANCEL ORDER
# ===============================
@api_view(['POST'])
def cancel_order(request, order_id):
    try:
        user = get_user(request)

        order = Order.objects.get(id=order_id, user=user)

        reason = request.data.get("reason", "")

        order.status = "cancelled"
        order.cancel_reason = reason
        order.save()

        return Response({"message": "Order cancelled"})

    except Order.DoesNotExist:
        return Response({"error": "Order not found"}, status=404)

# ===============================
# CREATE PAYMENT
# ===============================
@api_view(['POST'])
def create_payment(request):

    user = get_user(request)

    # ✅ FIX
    cart_items = Cart.objects.filter(user=user)

    if not cart_items.exists():
        return Response({"error": "Cart is empty"}, status=400)

    total = sum(item.product.price * item.quantity for item in cart_items)
    amount = int(total * 100)

    payment = client.order.create({
        "amount": amount,
        "currency": "INR",
        "payment_capture": 1
    })

    return Response(payment)

# ===============================
# VERIFY PAYMENT
# ===============================
@api_view(['POST'])
def verify_payment(request):

    order_id = request.data.get("razorpay_order_id")
    payment_id = request.data.get("razorpay_payment_id")
    signature = request.data.get("razorpay_signature")

    secret = "s5imSJzeEbJAXBYjEK0ufmng"

    generated_signature = hmac.new(
        bytes(secret, 'utf-8'),
        bytes(f"{order_id}|{payment_id}", 'utf-8'),
        hashlib.sha256
    ).hexdigest()

    if generated_signature == signature:
        return Response({"status": "success"})
    else:
        return Response({"status": "failed"}, status=400)

# ===============================
# ORDER DETAIL
# ===============================
@api_view(['GET'])
def get_order_detail(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return Response({"error": "Order not found"}, status=404)

    items_data = []

    order_items = OrderItem.objects.filter(order=order)

    for item in order_items:
        items_data.append({
            "id": item.id,
            "product_id": item.product.id,
            "product_name": item.product.name,
            "product_image": item.product.image.url if item.product.image else "",
            "quantity": item.quantity,
            "price": item.price,
        })

    data = {
        "id": order.id,
        "total_price": order.total_price,
        "status": order.status,
        "created_at": order.created_at,
        "address": order.address,
        "payment_method": order.payment_method,
        "items": items_data
    }

    return Response(data)

# ===============================
# RETURN ORDER
# ===============================
@api_view(['POST'])
def return_order(request, order_id):
    try:
        user = get_user(request)

        order = Order.objects.get(id=order_id, user=user)

        reason = request.data.get("reason", "")

        order.status = "returned"
        order.cancel_reason = reason
        order.save()

        return Response({"message": "Order return requested"})

    except Order.DoesNotExist:
        return Response({"error": "Order not found"}, status=404)