from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from shopapp.models import Product, Order


def shop_index(request: HttpRequest) -> HttpResponse:
    products = [
        {"name": "Ноутбук", "price": 75000},
        {"name": "Смартфон", "price": 45000},
        {"name": "Планшет", "price": 30000},
    ]

    return render(request, 'shopapp/shop.html', {'products': products})


def products_list(request: HttpRequest) -> HttpResponse:
    products = Product.objects.all()
    return render(request, 'shopapp/products_list.html', {'products': products})


def orders_list(request: HttpRequest) -> HttpResponse:
    orders = Order.objects.all()
    return render(request, 'shopapp/orders_list.html', {'orders': orders})