from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


@login_required
def dashboard(request):
    #sementara redirect ke machine
    return redirect('maas:machines:index')
    
    context = {
        'title': 'Dashboard',
        'menu_active': 'dashboard',
    }
    return render(request, 'website/dashboard.html', context)
