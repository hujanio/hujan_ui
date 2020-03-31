import requests
import json
import sweetify

from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from hujan_ui.installers.models import Server
from .forms import AddServerForm


@login_required
def index(request):
    servers = Server.objects.all()
    context = {
        'title': 'Servers',
        'servers': servers,
        'system_ids': ",".join([s.system_id for s in servers]),
        'menu_active': 'add-server'
    }
    return render(request, 'installers/server.html', context)


@login_required
def add(request):
    form = AddServerForm(request.POST or None)

    if form.is_valid():
        form.save()
        sweetify.success(request, _(f"Successfully added server"), button='OK', icon='success')
        return redirect("installer:servers:index")

    context = {
        'title': 'Add Server',
        'form': form,
        'menu_active': 'add-server',
        'title_submit': 'Save Server',
        'col_size': '12',
    }
    return render(request, "installers/add-server.html", context)
