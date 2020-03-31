import requests
import json
import sweetify

from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from hujan_ui.installers.models import Inventory
from .forms import InventoryForm


@login_required
def index(request):
    inventories = Inventory.objects.select_related('server').all()
    context = {
        'title': 'Inventories',
        'inventories': inventories,
        'menu_active': 'inventories',
        'inventory_groups': Inventory.GROUP
    }
    return render(request, 'installers/inventory.html', context)


@login_required
def add(request):
    form = InventoryForm(request.POST or None)

    if form.is_valid():
        form.save()
        sweetify.success(request, _(f"Successfully added inventory"), button='OK', icon='success')
        return redirect("installer:inventories:index")

    context = {
        'title': 'Add Inventory',
        'form': form,
        'menu_active': 'inventories',
        'title_submit': 'Save Inventory',
        'col_size': '12',
    }
    return render(request, "installers/form.html", context)


@login_required
def edit(request, id):
    inventory = get_object_or_404(Inventory, id=id)
    form = InventoryForm(data=request.POST or None, instance=inventory)
    if form.is_valid():
        form.save()
        sweetify.success(request, _(f"Successfully edited inventory"), button='OK', icon='success')
        return redirect("installer:inventories:index")

    context = {
        'title': 'Edit Inventory',
        'form': form,
        'menu_active': 'inventories',
        'title_submit': 'Edit Inventory',
        'col_size': '12',
    }
    return render(request, "installers/form.html", context)


@login_required
def delete(request, id):
    inventory = get_object_or_404(Inventory, id=id)
    inventory.delete()
    sweetify.success(request, _(f"Successfully deleted inventory"), icon='success', button='OK')
    return redirect("installer:inventories:index")
