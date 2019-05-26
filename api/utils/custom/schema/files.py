from marshmallow import fields

from api.utils.custom.schema.base import (BaseSchema, Timestamp)


class DownloadSchema(BaseSchema):
    filename = fields.String(required=False)
    mould_id = fields.String()

    class Meta:
        strict = True
