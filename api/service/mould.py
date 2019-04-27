from flask_security import roles_accepted
from webargs.flaskparser import use_args

from api.models import Mould, Aggregation
from api.utils.custom.error import error
from api.utils.custom.validators import validate_valid_layer_id
from api.utils.custom.interface_tips import InterfaceTips
from api.utils.custom.constants import LAYERS_CONFIG
from api.utils.custom.resource import BaseResource
from api.utils.custom.schema import (
    moulds_schema, mould_schema, base_query_schema, moulds_base_schema, mould_node_schema, mould_nodes_schema
)


class AggregationMouldsResource(BaseResource):
    @use_args(base_query_schema)
    @roles_accepted('admin')
    @BaseResource.check_record(Aggregation, 'aggregation_id', '集合')
    def get(self, args, layer_id, aggregation_id):
        if not validate_valid_layer_id(layer_id):
            error(InterfaceTips.INVALID_LAYER_ID)
        aggregation = self.record
        page = args.get('page', 1)
        per_page = args.get('per_page', 20)
        moulds, total = Mould.pagination(page, per_page, layer_id=layer_id, aggregation=aggregation)
        return BaseResource.pagination(moulds_schema.dump(moulds).data, total, per_page)

    @use_args(mould_schema)
    @roles_accepted('admin')
    @BaseResource.check_record(Aggregation, 'aggregation_id', '集合')
    def post(self, args, layer_id, aggregation_id):
        if not validate_valid_layer_id(layer_id):
            error(InterfaceTips.INVALID_LAYER_ID)
        aggregation = self.record
        if Mould.existed_record(code=args.get('code'), name=args.get('name')):
            error(InterfaceTips.RECORD_HAS_EXISTED)
        parent_id = args.pop('parent_id', None)
        if parent_id:
            parent = Mould.find_by_pk(parent_id)
            if not parent:
                error(InterfaceTips.PARENT_DATA_NOT_EXISTED)
            else:
                args.update({'parent': parent})
        bridge_ids = args.pop('bridge_ids', [])
        if bridge_ids:
            bridges = Mould.find_by_pks(bridge_ids)
            args.update({'bridges': bridges})
        args.update({'aggregation': aggregation, 'layer_id': layer_id})
        mould = Mould.create(**args)
        return mould_schema.dump(mould).data, 201


class MouldsResource(BaseResource):
    @roles_accepted('admin')
    def get(self):
        moulds = Mould.fetch_all()
        return moulds_base_schema.dump(moulds).data


class MouldResource(BaseResource):
    @roles_accepted('admin')
    @BaseResource.check_record(Mould, 'mould_id', '模型信息')
    def get(self, mould_id):
        mould = self.record
        return mould_schema.dump(mould).data

    @use_args(mould_schema)
    @roles_accepted('admin')
    @BaseResource.check_record(Mould, 'mould_id', '模型信息')
    def put(self, args, mould_id):
        layer_id = args.get('layer_id', None)
        if layer_id and not validate_valid_layer_id(layer_id):
            error(InterfaceTips.INVALID_LAYER_ID)
        mould = self.record
        if not args:
            error(InterfaceTips.NO_PARAMS)
        if Mould.existed_record(mould, code=args.get('code'), name=args.get('name')):
            error(InterfaceTips.RECORD_HAS_EXISTED)
        aggregation_id = args.pop('aggregation_id', None)
        if aggregation_id:
            aggregation = Aggregation.find_by_pk(aggregation_id)
            if aggregation:
                args.update({'aggregation': aggregation})
            else:
                error(InterfaceTips.AGGREGATION_NOT_EXISTED)

        parent_id = args.pop('parent_id', None)
        if parent_id:
            parent = Mould.find_by_pk(parent_id)
            if not parent:
                error(InterfaceTips.PARENT_DATA_NOT_EXISTED)
            else:
                args.update({'parent': parent})

        bridge_ids = args.pop('bridge_ids', [])
        if bridge_ids:
            bridges = Mould.find_by_pks(bridge_ids)
            args.update({'bridges': bridges})
        mould = mould.update(**args)
        children = mould_schema.dump(mould).data
        return children

    @roles_accepted('admin')
    @BaseResource.check_record(Mould, 'mould_id', '模型信息')
    def delete(self, mould_id):
        mould = self.record
        mould.delete()
        return {}, 204


class MouldTreeResource(BaseResource):
    @roles_accepted('admin')
    def get(self, layer_id):
        if not validate_valid_layer_id(layer_id):
            error(InterfaceTips.INVALID_LAYER_ID)
        moulds = Mould.get_ancestors(layer_id)
        children = mould_nodes_schema.dump(moulds).data
        layer_data = LAYERS_CONFIG.get(layer_id)
        mould_info = layer_data.get('mould_info')
        if children:
            mould_info.update({
                'has_children': bool(children),
                'children': children
            })
        return mould_info


class MouldParentResource(BaseResource):
    @roles_accepted('admin')
    @BaseResource.check_record(Mould, 'mould_id', '模型信息')
    def get(self, mould_id):
        mould = self.record
        return mould_schema.dump(mould.parent).data


class MouldChildrenResource(BaseResource):
    @roles_accepted('admin')
    @BaseResource.check_record(Mould, 'mould_id', '模型信息')
    def get(self, mould_id):
        mould = self.record
        children = mould.children
        return moulds_schema.dump(children).data
