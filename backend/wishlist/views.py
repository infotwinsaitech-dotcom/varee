from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from backend.products.models import Product
from .models import Wishlist

def get_user(request):
    if request.user.is_authenticated:
        return request.user
    user, _ = User.objects.get_or_create(username="guest_user")
    return user


# ✅ GET WISHLIST
@api_view(['GET'])
def get_wishlist(request):
    items = Wishlist.objects.all()

    data = []
    for item in items:
        data.append({
            "product": {
                "id": item.product.id,
                "name": item.product.name,
                "price": item.product.price,
                "image": item.product.image.url if item.product.image else ""
            }
        })

    return Response(data)


# ✅ ADD TO WISHLIST

@api_view(['POST'])
def add_to_wishlist(request):
    product_id = request.data.get("product_id")

    product = Product.objects.get(id=product_id)

    # duplicate avoid
    if not Wishlist.objects.filter(product=product).exists():
        Wishlist.objects.create(product=product)

    return Response({"message": "added"})
# ✅ REMOVE
@api_view(['POST'])
def remove_from_wishlist(request, product_id):
    Wishlist.objects.filter(product_id=product_id).delete()
    return Response({"message": "removed"})