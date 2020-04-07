import requests
import json
import sweetify

from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render, redirect, get_object_or_404
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
    form = AddServerForm(request.POST or None, instance=None)

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


@login_required
def edit(request, id):
    server = get_object_or_404(Server, id=id)
    form = AddServerForm(data=request.POST or None, instance=server)
    if form.is_valid():
        form.save()
        sweetify.success(request, _(f"Successfully edited server"), button='OK', icon='success')
        return redirect("installer:servers:index")

    context = {
        'title': 'Edit Server',
        'form': form,
        'menu_active': 'servers',
        'title_submit': 'Edit Server',
        'col_size': '12',
        'old_ip_address': server.ip_address
    }
    return render(request, "installers/add-server.html", context)


@login_required
def delete(request, id):
    server = get_object_or_404(Server, id=id)
    server.delete()
    sweetify.success(request, _(f"Successfully deleted server"), icon='success', button='OK')
    return redirect("installer:servers:index")
