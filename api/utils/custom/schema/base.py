import arrow

from marshmallow import (Schema, fields, post_dump)


class Timestamp(fields.DateTime):
    def _serialize(self, value, attr, obj):
        if value:
            return arrow.get(value).timestamp

    def _deserialize(self, value, attr, obj):
        return arrow.get(value).datetime


class BaseSchema(Schema):
    id = fields.Str(dump_only=True)
    updated_at = Timestamp(dump_only=True)
    created_at = Timestamp(dump_only=True)

    @post_dump
    def clear_none(self, data):
        result = {}
        for k, v in data.items():
            if v is None:
                continue
            elif isinstance(v, dict):
                result[k] = self.clear_none(v)
            else:
                result[k] = v
        return result


class BaseQuerySchema(Schema):
    page = fields.Int(missing=1)
    per_page = fields.Int(missing=10)
    q = fields.Str(location='query')

    class Meta:
        strict = True
