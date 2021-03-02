import sweetify

from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from hujan_ui.installers.models import Server, Installer
from hujan_ui.installers.decorators import deployment_checked
from .forms import AddServerForm


@login_required
@deployment_checked
def index(request):        
    servers = Server.objects.all()
    context = {
        'title': _('Servers'),
        'servers': servers,
        'system_ids': ",".join([s.system_id for s in servers]),
        'steps': Installer.get_steps,
        'menu_active': 'server',
    }
    return render(request, 'installers/server.html', context)


@login_required
@deployment_checked
def add(request):
    form = AddServerForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            sweetify.success(request, _("Successfully added server"), button='OK', icon='success')
        else:
            sweetify.error(request, _('Failed added server'))
        return redirect("installer:servers:index")
    context = {
        'title': _('Add Server'),
        'form': form,
        'steps': Installer.get_steps,
        'menu_active': 'server',
        'title_submit': _('Save Server'),
        'col_size': '12',
    }
    return render(request, "installers/add-server.html", context)


@login_required
@deployment_checked
def edit(request, id):
    server = get_object_or_404(Server, id=id)
    form = AddServerForm(data=request.POST or None, instance=server)
    if form.is_valid():
        form.save()
        sweetify.success(request, _("Successfully edited server"), button='OK', icon='success')
        return redirect("installer:servers:index")

    context = {
        'title': _('Edit Server'),
        'form': form,
        'steps': Installer.get_steps,
        'menu_active': 'server',
        'title_submit': _('Edit Server'),
        'col_size': '12',
        'old_ip_address': server.ip_address
    }
    return render(request, "installers/add-server.html", context)


@login_required
def delete(request, id):
    server = get_object_or_404(Server, id=id)
    server.delete()
    sweetify.success(request, _("Successfully deleted server"), icon='success', button='OK')
    return redirect("installer:servers:index")


@login_required
def reset(request):
    Server.objects.all().delete()
    sweetify.success(request, _('Successflully Reset Server'), icon='success', button='OK')
    return redirect("installer:servers:index")
