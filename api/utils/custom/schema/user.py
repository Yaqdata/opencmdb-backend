from marshmallow import fields

from api.utils.custom.schema.base import (BaseSchema, Timestamp)


class RoleSchema(BaseSchema):
    name = fields.String()
    description = fields.String()

    class Meta:
        strict = True


class UserBasicSchema(BaseSchema):
    email = fields.Email(required=True)

    class Meta:
        strict = True


class UserSchema(UserBasicSchema):
    password = fields.String(load_only=True)
    confirmed_at = Timestamp(dump_only=True)
    roles = fields.List(fields.Nested(RoleSchema))

    class Meta:
        strict = True
