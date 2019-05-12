import openstack


def get_connection(auth_url, username, password, project_name):
    return openstack.connect(
        auth_url=auth_url,
        project_name=project_name,
        username=username,
        password=password,
    )


def _get_instances(conn, limit, marker=None, show_detail=True):
    query_data = {
        'limit': limit,
        'detail': show_detail
    }
    if marker:
        query_data.update({'marker': marker})
    response = conn.compute.servers(**query_data)
    # TODO need return marker
    return response.servers, filter(lambda x: x.rel=='next', response.servers_links)


def get_openstack_instances(auth_url, username, password, project_name, limit=10, show_detail=True):
    conn = get_connection(auth_url, username, password, project_name)
    instances, marker = _get_instances(conn, limit, show_detail=show_detail)
    while marker:
        t_instances, marker = _get_instances(conn, limit, marker, show_detail)
        instances.extends(t_instances)
    return instances
