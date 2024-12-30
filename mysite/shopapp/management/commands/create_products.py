from django.core.management import BaseCommand
from shopapp.models import Product


class Command(BaseCommand):
    help = 'Create products'

    def handle(self, *args, **options):
        products = [
            {'name': 'Product 1', 'description': 'Description 1', 'price':
                100, 'quantity': 10},
            {'name': 'Product 2', 'description': 'Description 2', 'price':
                99, 'quantity': 5},
            {'name': 'Product 3', 'description': 'Description 3', 'price':
                259, 'quantity': 2},
            {'name': 'Product 4', 'description': 'Description 4', 'price':
                999, 'quantity': 25},
            {'name': 'Product 5', 'description': 'Description 5', 'price':
                5555, 'quantity': 3},
        ]

        for product_data in products:
            product, created = Product.objects.get_or_create(**product_data)
            if created:
                self.stdout.write(self.style.SUCCESS('Продукт создан'))
            else:
                self.stdout.write(f'Продукт {product.name} уже существует')