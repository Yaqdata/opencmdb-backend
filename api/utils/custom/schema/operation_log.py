from marshmallow import fields

from api.utils.custom.schema.base import (BaseSchema, BaseQuerySchema)
from api.utils.custom.schema.user import UserBasicSchema


class OperationLogSchema(BaseSchema):
    action = fields.Str()
    request_id = fields.Str()
    level = fields.Int()
    log_type = fields.Int()
    user = fields.Nested(UserBasicSchema, read_only=True)

    class Meta:
        strict = True


class OperationLogsQuerySchema(BaseQuerySchema):
    action = fields.Str(required=False)
    request_id = fields.Str(required=False)
    log_type = fields.Int(required=False)

    class Meta:
        strict = True
