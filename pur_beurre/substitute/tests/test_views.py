from django.contrib.auth.models import AnonymousUser
from django.db.models.query import QuerySet
from django.http import HttpRequest
from django.test import TestCase, RequestFactory
from django.urls import reverse, resolve
from substitute.models.product import Product
from substitute.models.user import User
from substitute.models.category import Category
from substitute.views import homepage
from substitute.services.searchsubstitute import SearchSubstitute
from substitute.services.favorite import Favorite


class HomePageTest(TestCase):
    """this class test the homepage"""
    def test_root_url_resolves_to_home_page_view(self):
        """this function test the homepage url"""
        found = resolve('/')
        self.assertEqual(found.func, homepage)

    def test_home_page_returns_correct_html(self):
        """this function test the homepage html"""
        request = HttpRequest()
        response = homepage(request)
        html = response.content.decode('utf8')
        self.assertIn('<title>Accueil</title>', html)


class SearchTestCase(TestCase):
    """this class test the search"""
    def setUp(self):
        Product.objects.create(name="chocolat", category_id=1)
        Product.objects.create(name="lait", category_id=1)
        Category.objects.create(name="snack", id=1)

    def test_template_return_unregistered_product(self):
        """this function test the unregistered product"""
        response = self.client.get("/search/", {'name_product': 'biscuit'})
        self.assertTemplateUsed(response, 'substitute/no_result.html')
        self.failUnlessEqual(response.status_code, 200)

    def test_template_return_registered_product(self):
        """this function test the registered product"""
        response = self.client.get("/search/", {'name_product': 'chocolat'})
        self.assertTemplateUsed(response, 'substitute/product.html')
        self.failUnlessEqual(response.status_code, 200)

    def test_product(self):
        """this function test product template, response code"""
        response = self.client.get("/search/", {'name_product': 'chocolat'})
        self.assertTemplateUsed(response, 'substitute/product.html')
        self.failUnlessEqual(response.status_code, 200)


class ProductTestCase(TestCase):
    """class product test"""
    def setUp(self):
        Product.objects.create(name="chocolat", category_id=1)
        Category.objects.create(name="snack", id=1)

    def test_product_404(self):
        """non-existent product number test"""
        response = self.client.get(reverse('product',
                                           kwargs={'pk': 676767676}))
        self.assertTemplateUsed(response, '404.html')
        self.failUnlessEqual(response.status_code, 404)

    def test_product_200(self):
        """existent product number test"""
        response = self.client.get(reverse('product', kwargs={'pk': 1}))
        self.assertTemplateUsed(response, 'substitute/product_detail.html')
        self.failUnlessEqual(response.status_code, 200)


class SearchSubstituteTestCase(TestCase):
    def setUp(self):
        Product.objects.create(name="chocolat",
                               image_url="url_chocolat",
                               nutriscore="b",
                               category_id=1)
        Product.objects.create(name="lait",
                               image_url="url_lait",
                               nutriscore="a",
                               category_id=1)
        Product.objects.create(name="biscuit",
                               image_url="url_biscuit",
                               nutriscore="b",
                               category_id=2)
        Category.objects.create(name="snack", id=1)
        Category.objects.create(name="fromage", id=2)
        self.factory = RequestFactory()
        self.request = self.factory.get(
            reverse("search", kwargs={}), {"name_product": "chocolat"})
        self.search = SearchSubstitute(self.request)

    def test_query_get_product_name(self):
        """test request product"""
        result = self.search._query_get_product_name()
        self.assertEqual(result, "chocolat")

    def test_save_search_product(self):
        """test saved request product"""
        search_product = self.search._save_search_product()
        self.assertEqual(type(search_product), QuerySet)

    def test_validate_search_product(self):
        """test validate_search_product() method"""
        self.assertTrue(self.search.validate_search_product())

    def test_get_product_substitute(self):
        """test get_product_substitute() method"""
        result = self.search.get_product_substitute()
        self.assertEqual(len(result), 1)


class SaveFavoriteTestCase(TestCase):
    """this class test the save favorite user case"""
    def setUp(self):
        Product.objects.create(pk=1,
                               name="biscuit",
                               image_url="url_biscuit",
                               nutriscore="b",
                               category_id=1)
        Category.objects.create(name="snack", id=1)
        self.factory = RequestFactory()
        self.user = User.objects.create_user(pk=1,
                                             username='jacob',
                                             email='jacob@orange.fr',
                                             password='top_secret')
        self.request = self.factory.get("save-favorite/1")
        self.favorite = Favorite(self.request, pk_prod=1)
        self.request.user = self.user

    def test_login_validate(self):
        """you must be authenticated to add a favorite"""
        # the user is logged in
        self.assertTrue(self.favorite.login_validate())
        # the user is logged out
        self.request.user = AnonymousUser()
        self.assertFalse(self.favorite.login_validate())

    def test_saved_favorite(self):
        """the function must add the favorites in the database"""
        self.favorite.saved_favorite()
        favorite_sub = Product.objects.get(favorite__id=1)
        self.assertEquals(favorite_sub.name, 'biscuit')

    def test_return_favorite_list(self):
        """the function must return a list"""
        self.favorite.saved_favorite()
        favorite_list = self.favorite.return_favorite_list()
        self.assertEqual(len(favorite_list), 1)
        self.assertEqual(favorite_list[0][0], 1)
        self.assertEqual(favorite_list[0][1], 'biscuit')
        self.assertEqual(favorite_list[0][2], 'url_biscuit')
        self.assertEqual(favorite_list[0][3], 'b')

    def test_view_save_favorite(self):
        """save favorite if the user is logged in"""
        self.client.login(username='jacob', password='top_secret')
        response = self.client.get(reverse('save_favorite',
                                           kwargs={'pk_prod': 1}))
        self.assertTemplateUsed(response, 'substitute/favorite.html')
        self.failUnlessEqual(response.status_code, 200)

    def test_view_favorite(self):
        """save favorite if the user is logged in"""
        self.client.login(username='jacob', password='top_secret')
        response = self.client.get(reverse('favorite'))
        self.assertTemplateUsed(response, 'substitute/favorite.html')
        self.failUnlessEqual(response.status_code, 200)
