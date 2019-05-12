from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkecs.request.v20140526 import DescribeInstancesRequest


def _get_instances(client, page, per_page):
    request = DescribeInstancesRequest.DescribeInstancesRequest()
    request.setPageNumber(per_page)
    request.setPageSize(page)
    try:
        response = client.do_action_with_exception(request)
    except ServerException as e:
        print(e)
    except ClientException as e:
        print(e)
    else:
        return response.get('Instances').get('Instance'), response.get('TotalCount') >= page * per_page


def get_aliyun_instances(access_key_id, access_key_secret, region_id, page=1, per_page=10):
    client = AcsClient(access_key_id, access_key_secret, region_id)
    instances, has_next = _get_instances(client, page, per_page)
    while has_next:
        page += 1
        t_instances, has_next = _get_instances(client, page, per_page)
        instances.extends(t_instances)
    return instances
