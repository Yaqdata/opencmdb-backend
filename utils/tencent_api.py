from tencentcloud.common import credential
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.cvm.v20170312 import cvm_client, models


def _get_instance(client, page, per_page):
    try:
        req = models.DescribeInstancesRequest(Offset=(page-1)*per_page, Limit=per_page)
        resp = client.DescribeInstances(req)
    except TencentCloudSDKException as err:
        print(err)
    else:
        return resp.InstanceSet, resp.TotalCount > page * per_page


def get_tencent_instances(secret_id, secret_key, region, page=1, per_page=10):
    cred = credential.Credential(secret_id, secret_key)
    client = cvm_client.CvmClient(cred, region)
    instances, has_next = _get_instance(client, page, per_page)
    while has_next:
        page += 1
        t_instances, has_next = _get_instance(client, page, per_page)
        instances.extends(t_instances)
    return instances
