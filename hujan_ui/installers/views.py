from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate


@login_required
def server(request):
    context = {
        'title': 'Servers',
        'menu_active': 'add-server'
    }
    return render(request, 'installers/server.html', context)


@login_required
def inventory(request):
    context = {
        'title': 'Inventory',
        'menu_active': 'inventory'
    }
    return render(request, 'installers/inventory.html', context)


@login_required
def global_config(request):
    context = {
        'title': 'Global Configuration',
        'menu_active': 'global-config'
    }
    return render(request, 'installers/global_config.html', context)


@login_required
def advanced_config(request):
    context = {
        'title': 'Advanced Configuration',
        'menu_active': 'advanced-config'
    }
    return render(request, 'installers/advanced_config.html', context)


@login_required
def deploy(request):
    context = {
        'title': 'Deploy',
        'menu_active': 'deploy'
    }
    return render(request, 'installers/deploy.html', context)
