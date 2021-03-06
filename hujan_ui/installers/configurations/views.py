import sweetify

from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models.fields import NOT_PROVIDED

from hujan_ui.installers.models import GlobalConfig, AdvancedConfig, Installer
from hujan_ui.installers.decorators import deployment_checked
from .forms import GlobalConfigForm, AdvancedConfigForm


@login_required
@deployment_checked
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
        'steps': Installer.get_steps,
        'menu_active': 'global_configuration',
        'form': form
    }
    return render(request, 'installers/global-config-form.html', context)


@login_required
def reset_global_config(request):
    global_config = GlobalConfig.objects.first()
    for f in global_config._meta.fields:
        if f.default:
            if f.default != NOT_PROVIDED:
                setattr(global_config, f.name, f.default)
            else:
                if f.name != "id":
                    setattr(global_config, f.name, "")
    global_config.save()
    sweetify.success(request, _("Successfully reset global configuration"), button='OK', icon='success')
    
    return redirect("installer:configurations:global_config")


@login_required
@deployment_checked
def advanced_config(request):
    advanced_config = AdvancedConfig.objects.all()
    Installer.set_step_advanced_config()

    context = {
        'title': _('Advanced Configuration'),
        'steps': Installer.get_steps,
        'menu_active': 'advanced_configuration',
        'advanced_config': advanced_config
    }
    return render(request, 'installers/advanced-config.html', context)


@login_required
@deployment_checked
def add_advanced_config(request):
    form = AdvancedConfigForm(request.POST or None)

    if form.is_valid():
        form.save()
        sweetify.success(request, _("Successfully added advanced configuration"), button='OK', icon='success')
        return redirect("installer:configurations:advanced_config")

    context = {
        'title': _('Add Advanced Configuration'),
        'form': form,
        'steps': Installer.get_steps,
        'menu_active': 'advanced_configuration',
        'title_submit': _('Save Advanced Configuration'),
        'col_size': '12',
    }
    return render(request, "installers/form.html", context)


@login_required
@deployment_checked
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
        'steps': Installer.get_steps,
        'menu_active': 'advanced_configuration',
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


@login_required
def reset_advanced_config(request):
    AdvancedConfig.objects.all().delete()
    sweetify.success(request, _("Successfully reset advanced configuration"), button='OK', icon='success')
    
    return redirect("installer:configurations:advanced_config")