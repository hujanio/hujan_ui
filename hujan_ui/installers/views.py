from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

from hujan_ui.installers.models import (
    Server, Inventory, GlobalConfig, AdvancedConfig,
    Deployment)
from hujan_ui.utils.deployer import Deployer


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
def deploy(request):
    context = {
        'title': 'Deploy',
        'menu_active': 'deploy',
        'servers': Server.objects.all(),
        'inventories': Inventory.objects.select_related('server').all(),
        'advanced_config': AdvancedConfig.objects.all(),
        'global_config': GlobalConfig.objects.first()
    }
    return render(request, 'installers/deploy.html', context)


@login_required
def do_deploy(request):
    deployer = Deployer()
    if not deployer.is_deploying():
        deployer.deploy()

    context = {
        "deployment": deployer.deployment_model
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
