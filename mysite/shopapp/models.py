from django.contrib.auth.models import User
from django.db import models

class Product(models.Model):
    """
    class Product
    """
    name = models.CharField(max_length=100)
    description = models.TextField(null=False, blank=True)
    price = models.DecimalField(default=0, max_digits=9, decimal_places=2)
    quantity = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'Название продукта {self.name} => ${self.price}'


class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.PROTECT)
    products = models.ManyToManyField(Product, related_name='orders')
    description = models.TextField()
    status = models.CharField(max_length=50, default='Pending')
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Order {self.id} for {self.customer.username}'
