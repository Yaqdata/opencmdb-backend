from marshmallow import fields

from api.utils.custom.schema.base import BaseSchema
from api.utils.custom.validators import validate_code


class AggregationSchema(BaseSchema):
    code = fields.Str(validate=validate_code, required=True)
    name = fields.Str(required=True)
    layer_id = fields.Str(load_only=True)

    class Meta:
        strict = True
