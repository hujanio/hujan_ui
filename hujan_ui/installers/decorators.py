from functools import wraps

from django.shortcuts import redirect

from hujan_ui.installers.models import Deployment


def deployment_checked(view_func):
    """
    Decorator for views that checks if deployment still in progress
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if Deployment.get_status() == Deployment.DEPLOY_SUCCESS:
            return redirect("installer:index")
        elif Deployment.get_status() == Deployment.POST_DEPLOY_IN_PROGRESS or \
                Deployment.get_status() == Deployment.DEPLOY_IN_PROGRESS:
            return redirect("installer:do_deploy")
        elif Deployment.get_status() == Deployment.POST_DEPLOY_SUCCESS:
            return redirect("installer:index")
        return view_func(request, *args, **kwargs)
    return _wrapped_view
