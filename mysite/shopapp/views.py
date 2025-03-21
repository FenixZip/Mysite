import logging

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.core.exceptions import PermissionDenied

from shopapp.models import Product, Order
from shopapp.forms import ProductForm, OrderForm

# ======= Вьюхи для ПРОДУКТОВ =======


log = logging.getLogger(__name__)


class ProductListView(ListView):
    """Отображение списка доступных продуктов"""
    model = Product
    template_name = "shopapp/products_list.html"
    context_object_name = "products"
    log.debug('Product detail view %s', Product)
    log.info('INFO')
    def get_queryset(self):
        return Product.objects.filter(is_available=True)  # Фильтруем только доступные продукты


class ProductDetailView(DetailView):
    """Отображение деталей продукта"""
    model = Product
    template_name = "shopapp/product_detail.html"
    context_object_name = "product"


class ProductCreateView(CreateView):
    """Создание нового продукта"""
    model = Product
    form_class = ProductForm
    template_name = "shopapp/product_form.html"
    success_url = reverse_lazy("shopapp:product_list")


class ProductUpdateView(UpdateView):
    """Обновление данных продукта"""
    model = Product
    form_class = ProductForm
    template_name = "shopapp/product_form.html"
    success_url = reverse_lazy("shopapp:product_list")


class ProductArchiveView(View):
    """Архивация продукта (soft delete)"""

    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        return render(request, "shopapp/product_archive.html", {"product": product})

    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        product.is_available = False
        product.save()
        return redirect("shopapp:product_list")


# ======= Вьюхи для ЗАКАЗОВ =======

class OrderListView(ListView):
    """Отображение списка заказов"""
    model = Order
    template_name = "shopapp/orders_list.html"
    context_object_name = "orders"


class OrderDetailView(DetailView):
    """Отображение деталей заказа"""
    model = Order
    template_name = "shopapp/order_detail.html"
    context_object_name = "order"


class OrderCreateView(CreateView):
    """Создание нового заказа"""
    model = Order
    form_class = OrderForm
    template_name = "shopapp/order_form.html"
    success_url = reverse_lazy("shopapp:order_list")


class OrderUpdateView(UpdateView):
    """Обновление данных заказа"""
    model = Order
    form_class = OrderForm
    template_name = "shopapp/order_form.html"
    success_url = reverse_lazy("shopapp:order_list")


class OrderDeleteView(DeleteView):
    """Удаление заказа"""
    model = Order
    template_name = "shopapp/order_confirm_delete.html"
    success_url = reverse_lazy("shopapp:order_list")


def shop_index(request):
    """Главная страница магазина"""

    return render(request, "shopapp/shop_index.html")



class ProductCreateView(PermissionRequiredMixin, CreateView):
    """Создание нового продукта (только с разрешением)"""
    model = Product
    form_class = ProductForm
    template_name = "shopapp/product_form.html"
    success_url = reverse_lazy("shopapp:product_list")
    permission_required = "shopapp.add_product"

    def form_valid(self, form):
        form.instance.created_by = self.request.user  # Назначаем владельца
        return super().form_valid(form)


class ProductUpdateView(PermissionRequiredMixin, UpdateView):
    """Редактирование продукта (только для владельцев или суперпользователей)"""
    model = Product
    form_class = ProductForm
    template_name = "shopapp/product_form.html"
    success_url = reverse_lazy("shopapp:product_list")
    permission_required = "shopapp.change_product"

    def dispatch(self, request, *args, **kwargs):
        product = self.get_object()

        if not request.user.is_superuser and request.user != product.created_by:
            raise PermissionDenied("Вы не можете редактировать этот продукт")

        return super().dispatch(request, *args, **kwargs)
