from django.contrib.auth.models import User
from django.core.management import BaseCommand

from shopapp.models import Product, Order


class Command(BaseCommand):
    help = 'Create orders'

    def handle(self, *args, **options):
        user = User.objects.first()
        if not user:
            self.stdout.write('Пользователь не найден. Сначала создайте пользователя.')
            return

        products = Product.objects.all()
        if not products.exists():
            self.stdout.write('Не найдено ни одного продукта. Сначала создайте продукты.')
            return

        order, created = Order.objects.get_or_create(
            customer=user,
            description='Образец заказа',
        )
        if created:
            order.products.set(products)
            order.save()
            self.stdout.write(self.style.SUCCESS(f'Заказ {order.id} созданный с продуктами'))
        else:
            self.stdout.write(f"Заказ {order.id} уже существует")