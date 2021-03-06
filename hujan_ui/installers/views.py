from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from hujan_ui.utils.core import check_status_deployment
from hujan_ui.utils.deployer import Deployer
from hujan_ui.installers.models import (
    Server, Inventory, GlobalConfig, AdvancedConfig,
    Deployment, Installer)
from hujan_ui.installers.decorators import deployment_checked
import sweetify
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages


@login_required
def index(request):
    status_dev = Deployment.get_status()
    if status_dev == Deployment.DEPLOY_IN_PROGRESS or \
       status_dev == Deployment.POST_DEPLOY_IN_PROGRESS or \
       status_dev is None:
        return redirect('installer:servers:index')
    pd_status, d_status = check_status_deployment()

    context = {
        'title': _('Configurations'),
        'steps': Installer.get_steps,
        'menu_active': '',
        'servers': Server.objects.all(),
        'inventories': Inventory.objects.select_related('server').all(),
        'advanced_config': AdvancedConfig.objects.all(),
        'global_config': GlobalConfig.objects.first(),
        'pd_status': pd_status,
        'd_status': d_status
    }
    return render(request, 'installers/index.html', context)


@login_required
def server(request):
    context = {
        'title': _('Servers'),
        'menu_active': 'add-server'
    }
    return render(request, 'installers/server.html', context)


@login_required
def inventory(request):
    context = {
        'title': _('Inventory'),
        'menu_active': 'inventory'
    }
    return render(request, 'installers/inventory.html', context)


@login_required
def global_config(request):
    context = {
        'title': _('Global Configuration'),
        'menu_active': 'global-config'
    }
    return render(request, 'installers/global_config.html', context)


@login_required
def advanced_config(request):
    context = {
        'title': _('Advanced Configuration'),
        'menu_active': 'advanced-config'
    }
    return render(request, 'installers/advanced_config.html', context)


@login_required
@deployment_checked
def deploy(request):
    context = {
        'title': _('Deployment'),
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

    pd_status, d_status = check_status_deployment()
    Installer.set_step_deployment()
    deployer = Deployer()
    if not deployer.is_deploying():
        messages.success(request, """Deployment was Successfully! RUN 'kolla-ansible post-deploy' on your controller 
        on press <b>Post Deploy</b> Button to generate admin password to access Horizon Dashboard 
        'http://controllerip' If you want to destroy cluster, press <b>Destroy</b> button""")
        deployer.deploy()

    context = {
        "deployment": deployer.deployment_model,
        'steps': 'deploying',
        'menu_active': 'deployment',
        'pd_status': pd_status,
        'd_status': d_status
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


@login_required
def reset_all(request):
    Installer.objects.all().delete()
    Server.objects.all().delete()
    Inventory.objects.all().delete()
    GlobalConfig.objects.all().delete()
    AdvancedConfig.objects.all().delete()
    Deployment.objects.all().delete()
    sweetify.success(request, _('Reset Successfully'), icon='success', button='OK')

    return redirect('installer:index')


@login_required
def destroy_config(request):
    deployer = Deployer()
    deployer.reset()
    Deployment.objects.all().delete()
    sweetify.success(request, _('Destroy Config Successfully'), icon='success', button='OK')

    return redirect('installer:index')


@login_required
def post_deploy(request):
    deployer = Deployer()
    deployer.post_deploy()
    sweetify.success(request, _('Post Deploy Successfully'), icon='success', button='OK')
    messages.success(request, 'Your deployment process is complete')
    return redirect('installer:index')
