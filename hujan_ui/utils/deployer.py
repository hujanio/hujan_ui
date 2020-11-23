import os
import subprocess
import threading

from django.conf import settings
from django.utils.datetime_safe import datetime
from django.db.models import Q
from hujan_ui.installers.models import Server, Inventory, GlobalConfig, Deployment
from hujan_ui.utils.global_config_writer import GlobalConfigWriter
from hujan_ui.utils.host_editor import HostEditor
from hujan_ui.utils.multinode_writer import MultiNodeWriter


class Deployer:
    log_dir = settings.DEPLOYMENT_LOG_DIR
    deploy_command = settings.DEPLOYMENT_COMMAND
    post_deploy_command = settings.DEPLOYMENT_COMMAND

    def __init__(self, deployment_model=None):
        if not deployment_model:
            self.deployment_model = self.current_deployment()
        else:
            self.deployment_model = deployment_model

    def current_deployment(self):
        """
        Get currently running deployment model
        """
        return Deployment.objects.filter(Q(status=Deployment.DEPLOY_IN_PROGRESS) | Q(status=Deployment.POST_DEPLOY_IN_PROGRESS)).first()

    def is_deploying(self):
        """
        Check if deploying in progress
        """
        return self.deployment_model is not None and self.deployment_model.status == Deployment.DEPLOY_IN_PROGRESS

    def get_log(self, from_line=0):
        """
        Get log lines from current deployment
        """
        assert self.deployment_model is not None

        if os.path.exists(self._log_file_path()):
            with open(self._log_file_path(), 'r') as f:
                lines = f.readlines()

            return lines[from_line:]
        else:
            return []

    def _prepare_log_dir(self):
        """
        Create log dir if not exist
        """
        if not os.path.exists(self.log_dir):
            os.mkdir(self.log_dir)

    def _write_log(self, line):
        """
        Write line to log file of deployment_model
        """
        with open(self._log_file_path(), 'a+') as f:
            f.write(line)

    def _log_file_path(self):
        """
        Return absolute log file path of current deployment model
        """
        return os.path.join(self.log_dir, self.deployment_model.log_name)

    def _output_reader(self, proc):
        """
        Read process output
        """
        self._write_log("Process Started\n")
        for line in iter(proc.stdout.readline, b''):
            line_str = line.decode('utf-8')
            self._write_log(line_str)

        proc.wait()
        return_code = proc.returncode

        self._write_log(f"Process exited with return code: {return_code}\n")

        if return_code == 0:
            self.deployment_model.status = Deployment.DEPLOY_SUCCESS
            self.deployment_model.save()
        else:
            self.deployment_model.status = Deployment.DEPLOY_FAILED
            self.deployment_model.save()

    def _output_reader_kolla(self, proc):
        self._write_log("Process Started\n")
        for line in iter(proc.stdout.readline, b''):
            line_str = line.decode('utf-8')
            self._write_log(line_str)

        proc.wait()
        return_code = proc.returncode

        self._write_log(f"Process exited with return code: {return_code}\n")

        if return_code == 0:
            self.deployment_model.status = Deployment.POST_DEPLOY_IN_PROGRESS
            self.deployment_model.save()
        else:
            self.deployment_model.status = Deployment.POST_DEPLOY_FAILED
            self.deployment_model.save()

    def _output_reader_post_deploy(self, proc):
        self._write_log("Process Started\n")
        for line in iter(proc.stdout.readline, b''):
            line_str = line.decode('utf-8')
            self._write_log(line_str)

        proc.wait()
        return_code = proc.returncode
        if return_code == 0:
            self.deployment_model.status = Deployment.POST_DEPLOY_SUCCESS
            self.deployment_model.save()
        else:
            self.deployment_model.status = Deployment.DEPLOY_FAILED
            self.deployment_model.save()
        self._write_log(f"Process post deploy exited with return code: {return_code}\n")

    def _start_process(self):
        """
        Start Process
        """
        proc = subprocess.Popen(self.deploy_command,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT)

        t = threading.Thread(target=self._output_reader, args=(proc,))
        t.start()

        return t

    def _start_kolla_deploy(self):
        proc_kolla = subprocess.Popen(settings.KOLLA_COMMAND_ALL,
                                      stdout=subprocess.PIPE,
                                      stderr=subprocess.STDOUT)

        t = threading.Thread(target=self._output_reader_kolla, args=(proc_kolla,))
        t.run()

    def _start_post_deploy(self):

        proc = subprocess.Popen(self.post_deploy_command,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT)
        t = threading.Thread(target=self._output_reader_post_deploy, args=(proc,))
        t.run()

    def _create_deployment(self):
        """
        Create deployment model
        """
        timestamp = datetime.now().strftime("%d%m%Y-%H%M%S")
        self.deployment_model = Deployment(
            log_name=f"deploy-log-{timestamp}.log",
            status=Deployment.DEPLOY_IN_PROGRESS
        )
        self.deployment_model.save()

    def _prepare_files(self):
        """
        Prepare file before deployment
        """
        HostEditor.save_from_model(Server.objects.all())
        MultiNodeWriter.save_from_model(Inventory.objects.all())
        GlobalConfigWriter.save_from_model(GlobalConfig.objects.first())

    def deploy(self):
        self._prepare_files()
        self._prepare_log_dir()
        self._create_deployment()
        self._start_process()
        self._start_kolla_deploy()

    def post_deploy(self):

        self._prepare_log_dir()
        self._start_post_deploy()

    def reset(self):
        cs = GlobalConfigWriter()
        he = HostEditor()
        mn = MultiNodeWriter()

        he.clear()
        he.save()
        mn.clear()
        cs.clear()
