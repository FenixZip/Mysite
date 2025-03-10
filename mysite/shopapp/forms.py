from django import forms
from django.contrib.auth.models import User


from shopapp.models import Product, Order


class ProductForm(forms.ModelForm):
    """Форма для создания продукта"""

    class Meta:
        model = Product
        fields = ('name', 'description', 'price',
                  'quantity', 'is_available')


class OrderForm(forms.ModelForm):
    """Форма для создания заказа"""

    customer_name = forms.CharField(
        max_length=255,
        required=True,
        label="ФИО"
    )
    customer_phone = forms.CharField(
        max_length=20,
        required=True,
        label="Телефон"
    )

    products = forms.ModelMultipleChoiceField(
        queryset=Product.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        label="Продукты"
    )

    class Meta:
        model = Order
        fields = ['customer_name', 'customer_phone', 'status', 'products']