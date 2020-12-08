from django.contrib.postgres.search import SearchQuery, SearchVector
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .forms import SearchProduct
from substitute.models.product import Product
from substitute.models.product import User


def homepage(request):
    """this function displays the home page"""
    form = SearchProduct()
    return render(request, 'substitute/index.html', {'form': form})


def search(request):
    """this function allows you to search for products"""
    query = request.GET['name_product']
    product_substitute = []
    search_product = Product.objects.annotate(
        search=SearchVector('name')).filter(search=SearchQuery(query))

    if len(search_product) != 0:
        product = search_product[0]
        product_category = str(product.category_id)
        product_img = product.image_url
        search_substitute = Product.objects.annotate(
            search=SearchVector('category_id'))\
            .filter(search=product_category)

        for p in search_substitute:
            product_substitute.append(
                [p.pk, p.name, p.image_url, p.nutriscore])
        return render(request, 'substitute/product.html',
                      {'product_substitute': product_substitute,
                       'product_img': product_img,
                       'search_product': query})
    else:
        return HttpResponse('pas de reponses dsl')


def product(request, pk):
    """this function returns displays a particular product"""
    product_detail = get_object_or_404(Product, pk=pk)
    return render(request, 'substitute/product_detail.html',
                  {'product': product_detail})


def save_favorite(request, pk_prod):
    """this function allows you to save a favorite"""
    if request.user.is_authenticated:
        pk_user = User.objects.get(pk=request.user.pk)
        pk_product = Product.objects.get(pk=pk_prod)
        pk_product.favorite.add(pk_user)
        product = []
        for p in Product.objects.filter(favorite__id=request.user.pk):
            product.append([p.pk, p.name, p.image_url, p.nutriscore])
        return render(request, 'substitute/favorite.html',
                  {'product': product})


def favorite(request):
    """this function is used to display the favorites"""
    if request.user.is_authenticated:
        product = []
        for p in Product.objects.filter(favorite__id=request.user.pk):
            product.append([p.pk, p.name, p.image_url, p.nutriscore])
        return render(request, 'substitute/favorite.html',
                      {'product': product})


def favorite_detail(request, pk):
    """this function is used to display the details of a favorite"""
    product_detail = get_object_or_404(Product, pk=pk)
    return render(request, 'substitute/favorite_detail.html',
                  {'product': product_detail})
