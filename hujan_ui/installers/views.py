from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate

from .forms import SignupForm


@login_required
def index(request):
    context = {
        'title': 'Dashboard',
        'menu_active': 'dashboard',
    }
    return render(request, 'installers/dashboard.html', context)


@login_required
def sales_order(request):
    context = {
        'title': 'Sales Order',
        'menu_active': 'sales',
    }
    return render(request, 'installers/sales_order.html', context)


@login_required
def returns_order(request):
    context = {
        'title': 'Returns Order',
        'menu_active': 'sales',
    }
    return render(request, 'installers/sales_order.html', context)


@login_required
def reports(request):
    context = {
        'title': 'Reports',
        'menu_active': 'sales',
    }
    return render(request, 'installers/report.html', context)


@login_required
def invoice(request):
    context = {
        'title': 'Invoice',
        'menu_active': 'sales',
    }
    return render(request, 'installers/invoice.html', context)


def signup(request):
    form = SignupForm(request.POST or None)
    if form.is_valid():
        form.save()
        username = form.cleaned_data.get('username')
        raw_password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=raw_password)
        login(request, user)
        return redirect('home')

    context = {
        'title': 'Register',
        'form': form
    }
    return render(request, 'registration/signup.html', context)
