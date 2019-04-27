import logging

from api.models.base import BasicDocument
from api.utils.common.extentions import db
from api.utils.custom.constants import OperationLogType


class OperationLog(BasicDocument):
    request_id = db.StringField(max_length=128, help_text='请求ID')
    action = db.StringField(max_length=255, help_text='操作')
    level = db.IntField(default=logging.INFO)
    log_type = db.IntField(default=OperationLogType.OPERATION_LOG.value)
    user = db.ReferenceField('User')
    log_data = db.DictField(help_text='记录data')
    request_url = db.StringField(max_length=255)
    request_method = db.StringField(max_length=128, help='request method')
