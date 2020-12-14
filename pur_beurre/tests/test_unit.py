from django.http import HttpRequest
from django.test import TestCase
from django.urls import reverse, resolve

from substitute.models.product import Product
from substitute.models.user import User
from substitute.models.category import Category
from substitute.views import homepage


class ProductTestCase(TestCase):
    """product test"""
    def setUp(self):
        Product.objects.create(name="chocolat", category_id=1)
        Category.objects.create(name="snack", id=1)

    def test_product_404(self):
        """non-existent product number test"""
        response = self.client.get(reverse('product', kwargs={'pk': 676767676}))
        self.failUnlessEqual(response.status_code, 404)

    def test_product_200(self):
        """existent product number test"""
        response = self.client.get(reverse('product', kwargs={'pk': 1}))
        self.failUnlessEqual(response.status_code, 200)


class CreateAccountTestCase(TestCase):
    """register test"""
    def test_register(self):
        response = self.client.get(reverse('register'))
        self.failUnlessEqual(response.status_code, 200)


class HomePageTest(TestCase):
    """homepage test"""
    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, homepage)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = homepage(request)
        html = response.content.decode('utf8')
        self.assertIn('<title>Pur Beurre</title>', html)

