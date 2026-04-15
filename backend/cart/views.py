from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from backend.products.models import Product
from .models import CartItem

# ✅ FIXED USER (SESSION BASED)
def get_user(request):
    if request.user.is_authenticated:
        return request.user

    # 🔥 session create
    if not request.session.session_key:
        request.session.create()

    session_key = request.session.session_key

    user, _ = User.objects.get_or_create(username=session_key)
    return user


# ===============================
# GET + ADD
# ===============================
@api_view(['GET', 'POST'])
def cart_list(request):
    user = get_user(request)

    if request.method == 'GET':
        items = CartItem.objects.filter(user=user)

        data = []
        for item in items:
            data.append({
                "id": item.id,
                "product": {
                    "id": item.product.id,
                    "name": item.product.name,
                    "price": item.product.price,
                    "image": item.product.image.url if item.product.image else "",
                    "category": str(item.product.category)
                },
                "quantity": item.quantity
            })

        return Response(data)

    if request.method == 'POST':
        product_id = request.data.get("product_id")

        if not product_id:
            return Response({"error": "Product ID required"}, status=400)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=404)

        cart_item, created = CartItem.objects.get_or_create(
            user=user,
            product=product
        )

        if not created:
            cart_item.quantity += 1
            cart_item.save()

        return Response({"message": "Added to cart"})


# ===============================
# UPDATE + DELETE
# ===============================
@api_view(['GET', 'PATCH', 'DELETE'])
def cart_detail(request, id):
    try:
        item = CartItem.objects.get(id=id)
    except CartItem.DoesNotExist:
        return Response({"error": "Item not found"}, status=404)

    if request.method == 'GET':
        return Response({
            "id": item.id,
            "quantity": item.quantity
        })

    if request.method == 'PATCH':
        qty = request.data.get("quantity")

        if not qty or int(qty) < 1:
            return Response({"error": "Invalid quantity"}, status=400)

        item.quantity = int(qty)
        item.save()

        return Response({"message": "Quantity updated"})

    if request.method == 'DELETE':
        item.delete()
        return Response({"message": "Item removed"})