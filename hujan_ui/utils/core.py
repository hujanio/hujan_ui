from hujan_ui.installers.models import Deployment


def conv_kb_to_mb(input_kilobyte):
    megabyte = 1./1000
    convert_mb = megabyte * input_kilobyte
    return convert_mb


def conv_mb_to_gb(input_megabyte):
    gigabyte = 1.0/1024
    convert_gb = gigabyte * input_megabyte
    return convert_gb


def check_status_deployment():
    status_dev = Deployment.get_status()
    pd_status = False
    d_status = True
    d_status = d_status if status_dev == Deployment.DEPLOY_SUCCESS else False
    pd_status = pd_status if status_dev == Deployment.POST_DEPLOY_IN_PROGRESS else True
    return pd_status, d_status
