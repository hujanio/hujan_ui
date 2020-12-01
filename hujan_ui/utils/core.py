from hujan_ui.installers.models import Deployment
import os


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
    d_status = False if status_dev == Deployment.DEPLOY_SUCCESS or \
        status_dev == Deployment.DEPLOY_IN_PROGRESS else True
    pd_status = False if status_dev == Deployment.POST_DEPLOY_IN_PROGRESS or \
        status_dev == Deployment.DEPLOY_SUCCESS else True
    return pd_status, d_status


def demote(user_uid, user_gid):
    def set_ids():
        os.setgid(user_gid)
        os.setuid(user_uid)

    return set_ids
