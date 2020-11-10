from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect

from hujan_ui.utils.deployer import Deployer
from hujan_ui.installers.models import (
    Server, Inventory, GlobalConfig, AdvancedConfig,
    Deployment, Installer)
from hujan_ui.installers.decorators import deployment_checked
import sweetify
from django.utils.translation import ugettext_lazy as _


@login_required
def index(request):
    if Deployment.get_status() != Deployment.DEPLOY_SUCCESS:
            return redirect("installer:servers:index")    

    context = {
        'title': 'Configurations',
        'steps': Installer.get_steps,
        'menu_active': '',
        'servers': Server.objects.all(),
        'inventories': Inventory.objects.select_related('server').all(),
        'advanced_config': AdvancedConfig.objects.all(),
        'global_config': GlobalConfig.objects.first()
    }
    return render(request, 'installers/index.html', context)


@login_required
def server(request):
    context = {
        'title': 'Servers',
        'menu_active': 'add-server'
    }
    return render(request, 'installers/server.html', context)


@login_required
def inventory(request):
    context = {
        'title': 'Inventory',
        'menu_active': 'inventory'
    }
    return render(request, 'installers/inventory.html', context)


@login_required
def global_config(request):
    context = {
        'title': 'Global Configuration',
        'menu_active': 'global-config'
    }
    return render(request, 'installers/global_config.html', context)


@login_required
def advanced_config(request):
    context = {
        'title': 'Advanced Configuration',
        'menu_active': 'advanced-config'
    }
    return render(request, 'installers/advanced_config.html', context)


@login_required
@deployment_checked
def deploy(request):
    context = {
        'title': 'Deployment',
        'steps': Installer.get_steps,
        'menu_active': 'deployment',
        'servers': Server.objects.all(),
        'inventories': Inventory.objects.select_related('server').all(),
        'advanced_config': AdvancedConfig.objects.all(),
        'global_config': GlobalConfig.objects.first()
    }
    return render(request, 'installers/deploy.html', context)


@login_required
def do_deploy(request):
    if Deployment.get_status() == Deployment.DEPLOY_SUCCESS:
            return redirect("installer:servers:index")   
            
    Installer.set_step_deployment()
    deployer = Deployer()
    if not deployer.is_deploying():
        deployer.deploy()

    context = {
        "deployment": deployer.deployment_model,
        'steps': 'deploying',
        'menu_active': 'deployment',
    }
    return render(request, 'installers/deploy_progress.html', context)


def deploy_log(request, id):
    from_line = request.GET.get("from_line", 0)
    deployment_model = get_object_or_404(Deployment, id=id)
    deployer = Deployer(deployment_model=deployment_model)
    return JsonResponse(data={
        "deployment": {
            "id": deployer.deployment_model.id,
            "status": deployer.deployment_model.status
        },
        "log": deployer.get_log(int(from_line))
    })


def reset_all(request):
    Installer.objects.all().delete()
    Server.objects.all().delete()
    Inventory.objects.all().delete()
    GlobalConfig.objects.all().delete()
    AdvancedConfig.objects.all().delete()
    Deployment.objects.all().delete()
    sweetify.success(request, _('Reset Successfully'), icon='success', button='OK')

    return redirect('installer:index')


def destroy_config(request):
    """
    docstring
    """
    pass
