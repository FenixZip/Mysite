from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from shopapp.models import Order, Product


def shop_index(request: HttpRequest) -> HttpResponse:
    return render(request, "shopapp/shop_index.html")


def products_list(request):
    # Получаем все активные продукты из базы данных
    products = Product.objects.filter(is_active=True)
    return render(request, 'shopapp/products_list.html', {'products': products})


def orders_list(request):
    # Получаем все заказы из базы данных
    orders = Order.objects.select_related('customer').prefetch_related('products')
    return render(request, 'shopapp/orders_list.html', {'orders': orders})