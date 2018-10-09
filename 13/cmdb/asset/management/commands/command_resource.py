#encoding:utf-8

import json
import os
import shutil
from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.plugins.callback import CallbackBase
import ansible.constants as C

from django.core.management import BaseCommand
from django.conf import settings
from asset.models import Host,Resource


class ResultCallback(CallbackBase):

    def __init__(self):
        super(ResultCallback,self).__init__()
        self._cache_host = {}

    def v2_runner_on_ok(self, result, **kwargs):
        if result.task_name == 'collect_host':
            facts = result._result.get('ansible_facts', {})
            ip = facts.get('ansible_default_ipv4', {}).get('address', '')
            self._cache_host[result._host.name] = ip    #主要是通过主机名去获取IP
            # print(self._cache_host)
        elif result.task_name == 'collect_copy':
            pass
        elif result.task_name == 'collect_command':  #task_name表示任务名称
            ip = self._cache_host.get(result._host.name)    #一台主机执行一次
            resource = result._result.get('stdout_lines',[])
            Resource.create_obj(ip,resource[0],resource[1])





class Command(BaseCommand):

    def handle(self,*args,**options):
        AnsibleOptions = namedtuple('AnsibleOptions',
                             ['connection', 'module_path', 'forks', 'become', 'become_method', 'become_user', 'check',
                              'diff'])
        ansible_options = AnsibleOptions(connection='smart', module_path=[], forks=10, become=None, become_method=None,
                          become_user=None, check=False, diff=False)

        loader = DataLoader()
        passwords = {}
        results_callback = ResultCallback()
        inventory = InventoryManager(loader=loader, sources=os.path.join(settings.BASE_DIR,'etc','hosts.txt')) # 剧本的位置)
        variable_manager = VariableManager(loader=loader, inventory=inventory)
        path_resource = '/tmp/resource.py'
        # ansible all -i etc/hosts -m setup
        play_source = {
            'name': "cmdb",
            'hosts': 'all',  # 在哪些主机上执行
            'gather_facts': 'no',
            'tasks': [  # 执行的任务列表
                {
                    'name': 'collect_host',  # 任务名称
                    'setup': ''  # 执行任务模块
                },
                {
                    'name': 'collect_copy',  # 任务名称
                    'copy': 'src={0} dest={1}'.format(os.path.join(settings.BASE_DIR,'etc','resource.py'),path_resource)  # 执行任务模块
                },
                {
                    'name': 'collect_command',  # 任务名称
                    'command': 'python {0}'.format(path_resource)  # 执行任务模块
                },
            ]
        }

        play = Play().load(play_source, variable_manager=variable_manager, loader=loader)
        tqm = None
        try:
            tqm = TaskQueueManager(
                inventory=inventory,
                variable_manager=variable_manager,
                loader=loader,
                options=ansible_options,
                passwords=passwords,
                stdout_callback=results_callback,
            )
            result = tqm.run(play)
        finally:
            if tqm is not None:
                tqm.cleanup()

            shutil.rmtree(C.DEFAULT_LOCAL_TMP, True)