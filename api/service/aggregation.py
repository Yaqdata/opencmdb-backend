from flask_security import roles_accepted
from webargs.flaskparser import use_args

from api.models import (Aggregation, Mould)
from api.utils.custom.error import error
from api.utils.custom.interface_tips import InterfaceTips
from api.utils.custom.validators import validate_valid_layer_id
from api.utils.custom.resource import BaseResource
from api.utils.custom.schema import (aggregations_schema, aggregation_schema, moulds_base_schema)


class AggregationsResource(BaseResource):
    @roles_accepted('admin')
    def get(self, layer_id):
        if not validate_valid_layer_id(layer_id):
            error(InterfaceTips.INVALID_LAYER_ID)
        aggregations, total = Aggregation.pagination(layer_id=layer_id)
        result = []
        for aggregation in aggregations:
            aggregation_data = aggregation_schema.dump(aggregation).data
            moulds = Mould.fetch_all(aggregation=aggregation)
            aggregation_data.update({'moulds': moulds_base_schema.dump(moulds).data})
            result.append(aggregation_data)
        return result

    @use_args(aggregation_schema)
    @roles_accepted('admin')
    def post(self, args, layer_id):
        if not validate_valid_layer_id(layer_id):
            error(InterfaceTips.INVALID_LAYER_ID)
        if Aggregation.existed_record(code=args.get('code'), name=args.get('name')):
            error(InterfaceTips.RECORD_HAS_EXISTED)
        args.update(layer_id=layer_id)
        aggregation = Aggregation.create(**args)
        return aggregation_schema.dump(aggregation).data, 201


class AggregationResource(BaseResource):
    @roles_accepted('admin')
    @BaseResource.check_record(Aggregation, 'aggregation_id', '集合')
    def get(self, aggregation_id):
        aggregation = self.record
        return aggregation_schema.dump(aggregation).data

    @use_args(aggregation_schema)
    @roles_accepted('admin')
    @BaseResource.check_record(Aggregation, 'aggregation_id', '集合')
    def put(self, args, aggregation_id):
        layer_id = args.get('layer_id', None)
        if layer_id and not validate_valid_layer_id(layer_id):
            error(InterfaceTips.INVALID_LAYER_ID)
        aggregation = self.record
        if Aggregation.existed_record(aggregation, code=args.get('code'), name=args.get('name')):
            error(InterfaceTips.RECORD_HAS_EXISTED)
        aggregation = aggregation.update(**args)
        return aggregation_schema.dump(aggregation).data

    @roles_accepted('admin')
    @BaseResource.check_record(Aggregation, 'aggregation_id', '集合')
    def delete(self, aggregation_id):
        aggregation = self.record
        aggregation.delete()
        return {}, 204
