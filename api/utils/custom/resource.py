from functools import wraps
from flask_restful import Resource

from api.utils.custom.error import error
from api.utils.custom.interface_tips import InterfaceTips


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
    def pagination(self, ob_list, total, per_page=20):
        return ob_list, 200, {
            'X-Total': total,
            'X-Per-Page': per_page
        }
