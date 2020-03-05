from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


@login_required
def dashboard(request):
    context = {
        'title': 'Dashboard',
        'menu_active': 'dashboard',
    }
    return render(request, 'website/dashboard.html', context)
