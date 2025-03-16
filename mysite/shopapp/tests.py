from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Permission
from shopapp.models import Order, Product

class OrderDetailViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username="testuser", password="testpass")
        permission = Permission.objects.get(codename="view_order")
        cls.user.user_permissions.add(permission)

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()
        super().tearDownClass()

    def setUp(self):
        self.client.login(username="testuser", password="testpass")
        # Исправляем: создаем заказ с правильными полями
        self.order = Order.objects.create(
            user=self.user  # Убедитесь, что поле `user` есть в Order
        )

    def tearDown(self):
        self.order.delete()

    def test_order_details(self):
        url = reverse("shopapp:order_detail", kwargs={"pk": self.order.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["order"].pk, self.order.pk)


class OrdersExportTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.staff_user = User.objects.create_user(username="staffuser", password="staffpass", is_staff=True)

    @classmethod
    def tearDownClass(cls):
        cls.staff_user.delete()
        super().tearDownClass()

    def setUp(self):
        self.client.login(username="staffuser", password="staffpass")
        # Исправляем: добавляем `created_by`
        self.product = Product.objects.create(name="Test Product", price=100, created_by=self.staff_user)
        self.order = Order.objects.create(user=self.staff_user)  # Обязательно передаем user
        self.order.products.add(self.product)

    def tearDown(self):
        self.order.delete()
        self.product.delete()

    def test_orders_export(self):
        url = reverse("shopapp:orders_export")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        json_data = response.json()
        self.assertIn("orders", json_data)
        self.assertEqual(len(json_data["orders"]), 1)

        order_data = json_data["orders"][0]
        self.assertEqual(order_data["id"], self.order.id)
        self.assertEqual(order_data["user_id"], self.staff_user.id)
        self.assertEqual(order_data["product_ids"], [self.product.id])
