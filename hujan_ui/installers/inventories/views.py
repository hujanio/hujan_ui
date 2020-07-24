import sweetify
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import ugettext_lazy as _

from hujan_ui.installers.models import Inventory, Installer
from .forms import InventoryForm


@login_required
def index(request):
    inventories = Inventory.objects.select_related('server').all()
    context = {
        'title': _('Inventories'),
        'inventories': inventories,
        'steps': Installer.get_steps,
        'menu_active': 'inventory',
    }
    return render(request, 'installers/inventory.html', context)


@login_required
def add(request):
    form = InventoryForm(request.POST or None)

    if form.is_valid():
        form.save()
        sweetify.success(request, _("Successfully added inventory"), button='OK', icon='success')
        return redirect("installer:inventories:index")

    context = {
        'title': _('Add Inventory'),
        'form': form,
        'steps': Installer.get_steps,
        'menu_active': 'inventory',
        'title_submit': _('Save Inventory'),
        'col_size': '12',
    }
    return render(request, "installers/form.html", context)


@login_required
def edit(request, id):
    inventory = get_object_or_404(Inventory, id=id)
    form = InventoryForm(data=request.POST or None, instance=inventory)
    if form.is_valid():
        form.save()
        sweetify.success(request, _("Successfully edited inventory"), button='OK', icon='success')
        return redirect("installer:inventories:index")

    context = {
        'title': _('Edit Inventory'),
        'form': form,
        'steps': Installer.get_steps,
        'menu_active': 'inventory',
        'title_submit': _('Edit Inventory'),
        'col_size': '12',
    }
    return render(request, "installers/form.html", context)


@login_required
def delete(request, id):
    inventory = get_object_or_404(Inventory, id=id)
    inventory.delete()
    sweetify.success(request, _("Successfully deleted inventory"), icon='success', button='OK')
    return redirect("installer:inventories:index")
