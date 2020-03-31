import requests
import json
import sweetify

from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render, redirect
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
        sweetify.success(request, _(f"Successfully added inventory"), button='Ok', timer=2000)
        return redirect("installer:inventories:index")

    context = {
        'title': 'Add Inventory',
        'form': form,
        'menu_active': 'inventories',
        'title_submit': 'Save Inventory',
        'col_size': '12',
    }
    return render(request, "installers/form.html", context)
