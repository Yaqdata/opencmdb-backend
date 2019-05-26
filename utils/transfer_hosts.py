from api.models import Mould, Instance
from utils.aliyun_api import get_aliyun_instances
from utils.openstack_api import get_openstack_instances
from utils.tencent_api import get_tencent_instances
from utils.aws_api import get_aws_instances


class TransferHosts(object):
    def __init__(self, mould_id):
        self.mould = Mould.find_by_pk(mould_id)

    def _transfer_instance(self, mould, instances):
        for instance in instances:
            Instance.update_or_create(mould=mould, abilities=instance)

    def transfer_aliyun_instances(self, access_key_id, access_key_secret, region_id):
        ali_instances = get_aliyun_instances(access_key_id, access_key_secret, region_id)
        self._transfer_instance(self.mould, ali_instances)

    def transfer_openstack_instances(self, auth_url, username, password, project_name):
        openstack_instances = get_openstack_instances(auth_url, username, password, project_name)
        self._transfer_instance(self.mould, openstack_instances)

    def transfer_tencent_instances(self, secret_id, secret_key, region):
        tencent_instances = get_tencent_instances(secret_id, secret_key, region)
        self._transfer_instance(self.mould, tencent_instances)

    def transfer_aws_instance(self):
        aws_instances = get_aws_instances()
        self._transfer_instance(self.mould, aws_instances)


def transfer_hosts_manager(instance, mould_id):
    transfer_hosts = TransferHosts(mould_id)
    transfer_hosts.transfer_aliyun_instances(**instance.abilities)
