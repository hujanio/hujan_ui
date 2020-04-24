import sweetify

from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from hujan_ui.installers.models import GlobalConfig
from .forms import GlobalConfigForm


@login_required
def global_config(request):
    global_config = GlobalConfig.objects.first()
    if not global_config:
        global_config = GlobalConfig.objects.create()
    form = GlobalConfigForm(request.POST or None, instance=global_config)
    if form.is_valid():
        form.save()
        sweetify.success(request, _(f"Successfully update global config"), button='OK', icon='success')
        return redirect("installer:configurations:global_config")

    context = {
        'title': 'Global Configuration',
        'menu_active': 'global-configuration',
        'form': form
    }
    return render(request, 'installers/global-config-form.html', context)
