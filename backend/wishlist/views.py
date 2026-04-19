from rest_framework.decorators import api_view
from rest_framework.response import Response
from backend.products.models import Product
from .models import Wishlist

# ✅ LIST

@api_view(['GET'])
def wishlist_list(request):

    items = Wishlist.objects.filter(user=request.user)

    data = []

    for item in items:
        data.append({
            "id": item.product.id,
            "name": item.product.name,
            "price": item.product.price,
            "image": item.product.image.url
        })

    return Response(data)


# ✅ ADD
@api_view(['POST'])
def add_to_wishlist(request, product_id):

    if not request.user.is_authenticated:
        return Response({"error": "Login required"}, status=403)

    product = Product.objects.get(id=product_id)

    Wishlist.objects.get_or_create(
        user=request.user,
        product=product
    )

    return Response({"message": "Added"})


# ✅ REMOVE
@api_view(['POST'])
def remove_from_wishlist(request, product_id):

    if not request.user.is_authenticated:
        return Response({"error": "Login required"}, status=403)

    Wishlist.objects.filter(
        user=request.user,
        product_id=product_id
    ).delete()

    return Response({"message": "Removed"})