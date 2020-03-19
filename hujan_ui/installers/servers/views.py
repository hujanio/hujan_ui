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
        form.clean()
        sweetify.warning(request, _("test"), button='Ok', timer=5000)

    context = {
        'title': 'Add Server',
        'form': form,
        'menu_active': 'add-server',
        'title_submit': 'Save Server',
        'col_size': '12'
    }
    return render(request, "installers/form.html", context)
