from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product, Category


# ===============================
# 🛍️ GET PRODUCTS + FILTER
# ===============================
@api_view(['GET'])
def get_products(request):

    products = Product.objects.all()

    category = request.GET.get('category')
    price = request.GET.get('price')

    if category:
        products = products.filter(category__name__icontains=category)

    if price:
        products = products.filter(price__lte=price)

    data = []
    for p in products:
        data.append({
            "id": p.id,
            "name": p.name,
            "price": p.price,
            "image": p.image.url if p.image else "",
            "category": p.category.name if p.category else ""
        })

    return Response(data)


# ===============================
# 🔍 SINGLE PRODUCT
# ===============================
@api_view(['GET'])
def get_product_detail(request, id):
    try:
        p = Product.objects.get(id=id)

        return Response({
            "id": p.id,
            "name": p.name,
            "price": p.price,
            "image": p.image.url if p.image else "",
            "description": p.description,
            "category": p.category.name if p.category else ""
        })

    except Product.DoesNotExist:
        return Response({"error": "Not found"}, status=404)


# ===============================
# 📂 GET CATEGORIES
# ===============================
@api_view(['GET'])
def get_categories(request):

    categories = Category.objects.all()

    data = []
    for c in categories:
        data.append({
            "id": c.id,
            "name": c.name
        })

    return Response(data)


# ===============================
# ➕ ADD PRODUCT (🔥 NEW)
# ===============================
@api_view(['POST'])
def add_product(request):

    name = request.data.get("name")
    price = request.data.get("price")
    category_name = request.data.get("category")
    image = request.FILES.get("image")

    if not name or not price:
        return Response({"error": "Name & Price required"}, status=400)

    # ✅ category handle
    category = None
    if category_name:
        category, _ = Category.objects.get_or_create(name=category_name)

    # ✅ create product
    product = Product.objects.create(
        name=name,
        price=price,
        category=category,
        image=image
    )

    return Response({
        "message": "Product added",
        "id": product.id
    })