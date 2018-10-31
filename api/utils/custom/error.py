from webargs.flaskparser import abort

from api.utils.custom.interface_tips import InterfaceTips


def error(error_info=InterfaceTips.INVALID_REQUEST, errors=None):
    http_code, error_code, error_msg = error_info.value
    params = {
        'message': error_msg,
        'errcode': error_code,
    }
    if errors:
        params['errors'] = errors

    abort(http_code, **params)
