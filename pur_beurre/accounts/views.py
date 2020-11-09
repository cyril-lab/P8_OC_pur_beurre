from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect

# Create your views here.
from django.template import loader
from django.http import HttpResponse
from django.http import HttpResponseRedirect

from .forms import CreateUserForm

from django.contrib.auth.models import User

from django.contrib.auth import logout


def register(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = CreateUserForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            name = form.cleaned_data['name']
            surname = form.cleaned_data['surname']
            email = form.cleaned_data['email']
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']
            username = email

            if password1 != password2:
                messages.warning(request, '. Saisissez des mots de passe identiques')
            else:
                user = User.objects.create_user(username, email, password1, first_name=name, last_name=surname)
                user.save()
                # return render(request, 'accounts/register.html', {'form': form})
                return redirect('login')

        return render(request, 'accounts/register.html', {'form': form})

    else:
        form = CreateUserForm()
        return render(request, 'accounts/register.html', {'form': form})


def login_user(request):
    if request.user.is_authenticated:
        return redirect('homepage')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('homepage')
            else:
                messages.info(request, 'Email ou mot de passe incorrect')

        context = {}
        return render(request, 'accounts/login.html', context)


def logout_user(request):
    logout(request)
    #messages.add_message(request, messages.SUCCESS, "Vous êtes déconnecté !")
    return redirect('homepage')


def account_user(request):

    return render(request, 'accounts/account.html')