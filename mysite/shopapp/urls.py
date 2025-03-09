from django.urls import path

from shopapp.views import shop_view

app_name = 'shopapp'

urlpatterns = [
    path('', shop_view, name='shop_view'),
]
