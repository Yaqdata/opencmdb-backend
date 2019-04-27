from flask_security import roles_accepted
from webargs.flaskparser import use_args

from api.models import OperationLog
from api.utils.custom.resource import BaseResource
from api.utils.custom.schema import (base_query_schema, operation_logs_schema)


class OperationLogsResource(BaseResource):
    @use_args(base_query_schema)
    @roles_accepted('admin')
    def get(self, args):
        logs, total = OperationLog.pagination(**args)
        return BaseResource.pagination(operation_logs_schema.dump(logs).data, total, args.get('per_page'))
