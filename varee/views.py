from django.shortcuts import render

def home(request):
    return render(request, "index.html")
@login_required
def orders_page(request):
    return render(request, "orders.html")
def order_detail(request, id):
    return render(request, "order_detail.html")
def product_detail(request, id):
    return render(request, 'product_detail.html')


