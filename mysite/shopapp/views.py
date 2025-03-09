from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def shop_view(request: HttpRequest) -> HttpResponse:
    products = [
        {"name": "Ноутбук", "price": 75000},
        {"name": "Смартфон", "price": 45000},
        {"name": "Планшет", "price": 30000},
    ]

    return render(request, 'shopapp/shop.html', {'products': products})
