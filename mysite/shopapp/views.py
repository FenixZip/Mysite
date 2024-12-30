from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from shopapp.models import Order


def shop_index(request: HttpRequest) -> HttpResponse:
    return render(request, "shopapp/shop_index.html")


def products_list(request: HttpRequest) -> HttpResponse:
    return render(request, "shopapp/products_list.html")


def orders_list(request: HttpRequest) -> HttpResponse:
    orders = Order.objects.select_related('customer').prefetch_related('products')
    return render(request, "shopapp/orders_list.html")