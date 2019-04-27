from marshmallow import fields

from api.utils.custom.schema.base import BaseSchema
from api.utils.custom.schema.aggregation import AggregationSchema
from api.utils.custom.validators import validate_code


class AttributeOptionSchema(BaseSchema):
    name = fields.Str()
    code = fields.Str()
    checked = fields.Bool()

    class Meta:
        strict = True


class AttributeSchema(BaseSchema):
    attribute_code = fields.Str(required=True)
    attribute_name = fields.Str(required=True)
    required = fields.Bool(required=True)
    front_type = fields.Str(required=True)
    type = fields.Str()
    max_length = fields.Int()
    min_length = fields.Int()
    default = fields.Raw()
    regexp = fields.Str()
    value = fields.Str()
    max_value = fields.Int()
    min_value = fields.Int()
    precision = fields.Int()
    options = fields.List(fields.Nested(AttributeOptionSchema))
    default_selected = fields.List(fields.Str())

    class Meta:
        strict = True


class MatrixSchema(BaseSchema):
    matrix_code = fields.Str(validate=validate_code, required=True)
    matrix_name = fields.Str(required=True)
    attributes = fields.List(fields.Nested(AttributeSchema), required=True)

    class Meta:
        strict = True


class MouldBaseSchema(BaseSchema):
    code = fields.Str(validate=validate_code)
    name = fields.Str()

    class Meta:
        strict = True


class MouldSchema(MouldBaseSchema):
    aggregation_id = fields.Str(load_only=True)
    aggregation = fields.Nested(AggregationSchema, dump_only=True)
    description = fields.Str()
    matrix = fields.List(fields.Nested(MatrixSchema))
    parent_id = fields.Str(load_only=True)
    parent = fields.Nested(MouldBaseSchema, dump_only=True)
    layer_id = fields.Str(load_only=True)
    bridge_ids = fields.List(fields.Str(), required=False)
    bridges = fields.List(fields.Nested(MouldBaseSchema), dump_only=True)

    class Meta:
        strict = True


class MouldNodeSchema(MouldBaseSchema):
    has_children = fields.Bool(dump_only=True)
    children = fields.Nested('self', dump_only=True, many=True)

    class Meta:
        strict = True
