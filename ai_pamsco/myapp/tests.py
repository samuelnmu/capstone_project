# tests.py
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import CustomUser, Product, Order, MarketPrice

class UserTests(APITestCase):
    def setUp(self):
        # Create admin user
        self.admin = CustomUser.objects.create_superuser(
            username="adminuser", email="admin@example.com", role="admin", location="HQ", password="adminpass"
        )
        # Create regular user
        self.user = CustomUser.objects.create_user(
            username="testuser", email="user@example.com", role="buyer", location="Nairobi", password="userpass"
        )

    def test_admin_can_list_users(self):
        self.client.login(email="admin@example.com", password="adminpass")
        url = reverse('user-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 2)

    def test_regular_user_can_only_see_themselves(self):
        self.client.login(email="user@example.com", password="userpass")
        url = reverse('user-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['email'], "user@example.com")


class ProductTests(APITestCase):
    def setUp(self):
        self.farmer = CustomUser.objects.create_user(
            username="farmer1", email="farmer@example.com", role="farmer", location="Nairobi", password="farmerpass"
        )
        self.client.login(email="farmer@example.com", password="farmerpass")

    def test_create_product(self):
        url = reverse('product-list')
        data = {
            "name": "Maize",
            "description": "Fresh maize",
            "price": "100.50",
            "quantity": 10,
            "category": "grains",
            "location": "Nairobi"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['farmer'], self.farmer.username)

    def test_list_products(self):
        Product.objects.create(
            name="Rice", description="Organic rice", price=200, quantity=5,
            category="grains", farmer=self.farmer, location="Nairobi"
        )
        url = reverse('product-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)


class OrderTests(APITestCase):
    def setUp(self):
        self.buyer = CustomUser.objects.create_user(
            username="buyer1", email="buyer@example.com", role="buyer", location="Nairobi", password="buyerpass"
        )
        self.farmer = CustomUser.objects.create_user(
            username="farmer1", email="farmer@example.com", role="farmer", location="Nairobi", password="farmerpass"
        )
        self.product = Product.objects.create(
            name="Beans", description="Red beans", price=50, quantity=20, category="grains", farmer=self.farmer, location="Nairobi"
        )
        self.client.login(email="buyer@example.com", password="buyerpass")

    def test_create_order(self):
        url = reverse('order-list')
        data = {"product": self.product.id, "quantity": 5}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['total_price'], "250.00")  # 50 * 5

    def test_list_orders_only_for_buyer(self):
        Order.objects.create(buyer=self.buyer, product=self.product, quantity=3, total_price=150)
        url = reverse('order-list')
        response = self.client.get(url)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['buyer'], self.buyer.username)


class MarketPriceTests(APITestCase):
    def setUp(self):
        self.admin = CustomUser.objects.create_superuser(
            username="adminuser", email="admin@example.com", role="admin", location="HQ", password="adminpass"
        )
        self.client.login(email="admin@example.com", password="adminpass")

    def test_create_market_price(self):
        url = reverse('marketprice-list')
        data = {"product_name": "Maize", "region": "Nairobi", "price": 100, "date_recorded": "2025-08-25"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['product_name'], "Maize")

    def test_list_market_prices(self):
        MarketPrice.objects.create(product_name="Rice", region="Nakuru", price=120, date_recorded="2025-08-20")
        url = reverse('marketprice-list')
        response = self.client.get(url)
        self.assertGreaterEqual(len(response.data), 1)
