import re

from marshmallow import ValidationError

from api.utils.custom.constants import LAYERS_CONFIG


def validate_code(s):
    pattern = re.compile(r'^[A-Za-z][A-Za-z0-9_]*$')
    match = re.match(pattern, s)
    if match is None:
        raise ValidationError('code: {} 格式不正确'.format(s))
    return s


def validate_valid_layer_id(layer_id):
    return layer_id in LAYERS_CONFIG
