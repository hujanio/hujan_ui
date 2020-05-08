import sweetify

from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from hujan_ui.installers.models import GlobalConfig, AdvancedConfig
from .forms import GlobalConfigForm, AdvancedConfigForm


@login_required
def global_config(request):
    global_config = GlobalConfig.objects.first()
    if not global_config:
        global_config = GlobalConfig.objects.create()
    form = GlobalConfigForm(request.POST or None, instance=global_config)
    if form.is_valid():
        form.save()
        sweetify.success(request, _("Successfully update global config"), button='OK', icon='success')
        return redirect("installer:configurations:global_config")

    context = {
        'title': _('Global Configuration'),
        'menu_active': 'global-configuration',
        'form': form
    }
    return render(request, 'installers/global-config-form.html', context)


@login_required
def advanced_config(request):
    advanced_config = AdvancedConfig.objects.all()

    context = {
        'title': _('Advanced Configuration'),
        'menu_active': 'advanced-configuration',
        'advanced_config': advanced_config
    }
    return render(request, 'installers/advanced-config.html', context)


@login_required
def add_advanced_config(request):
    form = AdvancedConfigForm(request.POST or None)

    if form.is_valid():
        form.save()
        sweetify.success(request, _("Successfully added advanced configuration"), button='OK', icon='success')
        return redirect("installer:configurations:advanced_config")

    context = {
        'title': _('Add Advanced Configuration'),
        'form': form,
        'menu_active': 'advanced-configuration',
        'title_submit': _('Save Advanced Configuration'),
        'col_size': '12',
    }
    return render(request, "installers/form.html", context)


@login_required
def edit_advanced_config(request, id):
    advanced_config = get_object_or_404(AdvancedConfig, id=id)
    form = AdvancedConfigForm(data=request.POST or None, instance=advanced_config)
    if form.is_valid():
        form.save()
        sweetify.success(request, _("Successfully edited advanced configuration"), button='OK', icon='success')
        return redirect("installer:configurations:advanced_config")

    context = {
        'title': _('Edit Advanced Configuration'),
        'form': form,
        'menu_active': 'advanced-configuration',
        'title_submit': _('Edit Advanced Configuration'),
        'col_size': '12',
    }
    return render(request, "installers/form.html", context)


@login_required
def delete_advanced_config(request, id):
    advanced_config = get_object_or_404(AdvancedConfig, id=id)
    advanced_config.delete()
    sweetify.success(request, _("Successfully deleted advanced configuration"), icon='success', button='OK')
    return redirect("installer:configurations:advanced_config")
