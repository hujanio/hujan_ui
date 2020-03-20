import requests
import json
import sweetify

from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .forms import AddServerForm


@login_required
def index(request):
    context = {
        'title': 'Servers',
        'menu_active': 'add-server'
    }
    return render(request, 'installers/server.html', context)


@login_required
def add(request):
    form = AddServerForm(request.POST or None)

    if form.is_valid():
        form.save()
        sweetify.success(request, _(f"Successfully added server"), button='Ok', timer=2000)
        return redirect("installer:servers:index")

    context = {
        'title': 'Add Server',
        'form': form,
        'menu_active': 'add-server',
        'title_submit': 'Save Server',
        'col_size': '12',
    }
    return render(request, "installers/add-server.html", context)
