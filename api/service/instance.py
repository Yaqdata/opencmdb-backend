from flask_security import roles_accepted
from webargs.flaskparser import use_args

from api.models import (Mould, Instance)
from api.utils.custom.error import error
from api.utils.custom.validators import validate_valid_layer_id
from api.utils.custom.constants import LAYERS_CONFIG
from api.utils.custom.interface_tips import InterfaceTips
from api.utils.custom.resource import BaseResource
from api.utils.custom.schema import (
    instance_schema, instances_schema, base_query_schema, instance_node_schema, instance_nodes_schema, mould_base_schema,
    instance_detail_schema, instances_detail_schema, bridges_instances_query_schema, mould_instances_stats_schema,
)
from utils.transfer_hosts import transfer_hosts_manager


class InstancesResource(BaseResource):
    @use_args(base_query_schema)
    @roles_accepted('admin')
    @BaseResource.check_record(Mould, 'mould_id', '模型')
    def get(self, args, mould_id):
        mould = self.record
        page = args.get('page', 1)
        per_page = args.get('per_page', 20)
        instances, total = Instance.pagination(page, per_page, mould=mould)
        return BaseResource.pagination(instances_detail_schema.dump(instances).data, total, args.get('per_page'))

    @use_args(instance_detail_schema)
    @roles_accepted('admin')
    @BaseResource.check_record(Mould, 'mould_id', '模型')
    def post(self, args, mould_id):
        mould = self.record
        success, error_message = mould.validate_abilities(args.get('abilities', {}))
        if not success:
            return error_message, 422

        parent_id = args.pop('parent_id', None)
        if mould.parent:
            if parent_id:
                parent = Instance.find_by_pk(parent_id)
                if not parent:
                    error(InterfaceTips.PARENT_DATA_NOT_EXISTED)
                args.update({'parent': parent})
            else:
                error(InterfaceTips.PARENT_ID_IS_REQUIRED)
        bridge_ids = args.pop('bridge_ids', [])
        if bridge_ids:
            bridges = Instance.find_by_pks(bridge_ids)
            args.update({'bridges': bridges})

        # TODO check record is existed
        # if Mould.existed_record(**args):
        #     error(InterfaceTips.RECORD_HAS_EXISTED)

        instance = Instance.create(mould=mould, **args)
        return instance_detail_schema.dump(instance).data, 201


class BridgesInstancesResource(BaseResource):
    @use_args(bridges_instances_query_schema)
    @roles_accepted('admin')
    def get(self, args):
        '''
        以应用维度查询资源信息
        '''
        mould_ids = args.pop('mould_ids', [])
        q = args.pop('q', None)
        if mould_ids:
            args.update({'mould__in': mould_ids})
        Instance.fetch_one()
        instances, total = Instance.pagination(**args)
        return BaseResource.pagination(instances_detail_schema.dump(instances).data, total, args.get('per_page'))


class MouldInstanceStatsResource(BaseResource):
    @use_args(mould_instances_stats_schema)
    @roles_accepted('admin')
    def get(self, args):
        '''
        以模型维统计资源信息
        :param args:
        :return:
        '''
        instances = Instance.fetch_all(**args)
        instance_aggregation = instances.aggregate(*[{'$group': {'_id': '$mould', 'count': {'$sum': 1}}}])
        moulds = Mould.fetch_all(**args)
        moulds_data = {}
        for mould in moulds:
            moulds_data.update({
                mould.id: mould_base_schema.dump(mould).data
            })
        mould_instances_stats = []
        for stats in instance_aggregation:
            stats_id = stats.pop('_id')
            stats.update({
                'mould': moulds_data.get(stats_id, {}),
                'id': str(stats_id)
            })
            mould_instances_stats.append(stats)
        return mould_instances_stats


class InstanceResource(BaseResource):
    @roles_accepted('admin')
    @BaseResource.check_record(Instance, 'instance_id', '实例')
    def get(self, instance_id):
        instance = self.record
        return instance_detail_schema.dump(instance).data

    @use_args(instance_schema)
    @roles_accepted('admin')
    @BaseResource.check_record(Instance, 'instance_id', '实例')
    def put(self, args, instance_id):
        layer_id = args.get('layer_id', None)
        if layer_id and not validate_valid_layer_id(layer_id):
            error(InterfaceTips.INVALID_LAYER_ID)
        instance = self.record
        success, error_message = instance.mould.validate_abilities(args.get('abilities', {}))
        if not success:
            return error_message, 422

        parent_id = args.pop('parent_id', None)
        if instance.mould.parent:
            if parent_id:
                parent = Instance.find_by_pk(parent_id)
                if not parent:
                    error(InterfaceTips.PARENT_DATA_NOT_EXISTED)
                args.update({'parent': parent})
            else:
                error(InterfaceTips.PARENT_ID_IS_REQUIRED)

        # if Mould.existed_record(instance, **args):
        #     error(InterfaceTips.RECORD_HAS_EXISTED)
        instance = instance.update(**args)
        return instance_detail_schema.dump(instance).data

    @roles_accepted('admin')
    @BaseResource.check_record(Instance, 'instance_id', '实例')
    def delete(self, instance_id):
        instance = self.record
        instance.delete()
        return {}, 204


class InstanceTreeResource(BaseResource):
    @roles_accepted('admin')
    def get(self, layer_id):
        if not validate_valid_layer_id(layer_id):
            error(InterfaceTips.INVALID_LAYER_ID)
        instances = Instance.get_ancestors(layer_id)
        children = instance_nodes_schema.dump(instances).data
        layer_data = LAYERS_CONFIG.get(layer_id)
        instance_info = layer_data.get('instance_info')
        if children:
            instance_info.update({
                'has_children': bool(children),
                'children': children
            })
        return instance_info


class InstanceParentResource(BaseResource):
    @roles_accepted('admin')
    @BaseResource.check_record(Instance, 'instance_id', '实例')
    def get(self, instance_id):
        instance = self.record
        return instance_detail_schema.dump(instance.parent).data


class InstanceChildrenResource(BaseResource):
    @roles_accepted('admin')
    @BaseResource.check_record(Instance, 'instance_id', '实例')
    def get(self, instance_id):
        instance = self.record
        return instances_schema.dump(instance.children).data


class CrawlInstances(BaseResource):
    @roles_accepted('admin')
    @BaseResource.check_record(Mould, 'mould_id', '模型')
    @BaseResource.check_record(Instance, 'instance_id', '实例')
    def put(self, instance_id, mould_id):
        instance = self.record
        transfer_hosts_manager(instance, mould_id)
        return {}
