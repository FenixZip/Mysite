from django.urls import path

from shopapp.views import shop_index, products_list, orders_list

app_name = 'shopapp'

urlpatterns = [
    path('', shop_index, name='shop_index'),
    path('products/', products_list, name='products_list'),
    path('orders/', orders_list, name='orders_list'),
]
