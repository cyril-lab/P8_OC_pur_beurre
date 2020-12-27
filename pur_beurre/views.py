from django.shortcuts import render


def homepage(request):
    """this function displays the home page"""
    return render(request, 'substitute/index.html')
