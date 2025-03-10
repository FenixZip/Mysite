from django.shortcuts import render
from django.urls import reverse

def shop_index(request):
    pages = {
        "Список продуктов": reverse("products_list"),
        "Список заказов": reverse("orders_list"),
    }
    return render(request, "shop_index.html", {"pages": pages})
