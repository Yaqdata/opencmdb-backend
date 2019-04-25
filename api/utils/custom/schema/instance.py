import copy

from marshmallow import fields

from api.utils.custom.schema.base import (BaseSchema, BaseQuerySchema)


class AbilityFiled(fields.Dict):
    def _serialize(self, value, attr, obj):
        result = copy.deepcopy(obj.mould.matrix)
        for mat in result:
            for attribute in mat.get('attributes'):
                if value.get(attribute.get('attribute_code')):
                    attribute.update({'attribute_value': value.get(attribute.get('attribute_code'))})
        return result


class InstanceSchema(BaseSchema):
    matrix = AbilityFiled(required=True, attribute='abilities', dump_only=True)
    abilities = fields.Dict(required=True, load_only=True)

    class Meta:
        strict = True


class InstanceDetailSchema(InstanceSchema):
    parent_id = fields.Str()
    parent = fields.Nested(InstanceSchema, dump_only=True)

    class Meta:
        strict = True


class InstanceNodeSchema(InstanceSchema):
    has_children = fields.Bool(dump_only=True)
    children = fields.Nested('self', dump_only=True, many=True)

    class Meta:
        strict = True


class BridgesInstancesQuerySchema(BaseQuerySchema):
    bridge_id = fields.Str()
    layer_id = fields.Str(default='5b13ef6080ac93f4bb3f892f')
    mould_ids = fields.List(fields.Str(), required=False)

    class Meta:
        strict = True


class MouldInstanceStatsSchema(BaseSchema):
    layer_id = fields.Str(default='5b13ef6080ac93f4bb3f892f')

    class Meta:
        strict = True
