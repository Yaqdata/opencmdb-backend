import inspect

from functools import wraps
from flask import request
from flask_log_request_id import current_request_id
from flask_restful import Resource
from flask_security import current_user

from api.utils.custom.error import error
from api.utils.custom.interface_tips import InterfaceTips
from api.models import (OperationLog, User)


class BaseResource(Resource):
    record = None

    @classmethod
    def check_record(cls, model, model_key, model_message=None):
        def decorate(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                record_id = kwargs.get(model_key, None)
                message = model_message if model_message else str(model)
                if record_id is None:
                    error(InterfaceTips.DATA_NOT_EXISTED, {'model': message})
                try:
                    record = model.find_by_pk(record_id)
                except Exception as e:
                    error(InterfaceTips.DATA_NOT_EXISTED, {'model': message})
                else:
                    if record is None:
                        error(InterfaceTips.DATA_NOT_EXISTED, {'model': message})
                    cls.record = record
                return func(*args, **kwargs)
            return wrapper
        return decorate

    @classmethod
    def pagination(cls, ob_list, total, per_page=20):
        return ob_list, 200, {
            'X-Total': total,
            'X-Per-Page': per_page
        }

    @classmethod
    def request_log(cls, action):
        def decorate(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                func_args = inspect.getfullargspec(func)[0]
                params = dict(zip(func_args, args))
                operation_log_data = {
                    'request_id': current_request_id(),
                    'action': action,
                    'request_url': request.path,
                    'request_method': request.method,
                    'log_data': params.get('args', {})
                }

                if isinstance(current_user, User):
                    operation_log_data.update({'user': current_user})
                OperationLog.create(**operation_log_data)
                return func(*args, **kwargs)
            return wrapper
        return decorate

