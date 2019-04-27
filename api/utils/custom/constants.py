from enum import Enum


class BasicEnum(Enum):
    @classmethod
    def values(cls):
        return [i.value for i in cls]

    @classmethod
    def keys(cls):
        return [i.name for i in cls]


class State(BasicEnum):
    DELETED = 0
    CREATED = 1


class OperationLogType(BasicEnum):
    OPERATION_LOG = 1


LAYERS_CONFIG = {
    '5b13ef6080ac93f4bb3f892f': {
        'name': '资源层',
        'mould_info': {
            'name': '资源模型',
            'has_children': False,
            'children': [],
        },
        'instance_info': {
            'has_children': False,
            'children': [],
            'matrix': [{
                "matrix_name": "基本属性",
                "attributes": [{
                    "attribute_name": "root",
                    "attribute_code": "name"
                }],
                "matrix_code": "group"
            }]
        }
    },
    '5b225e5c7c3b0567969d5f68': {
        'name': '应用层',
        'mould_info': {
            'name': '应用模型',
            'has_children': False,
            'children': [],
        },
        'instance_info': {
            'has_children': False,
            'children': [],
            'matrix': [{
                "matrix_name": "基本属性",
                "attributes": [{
                    "attribute_name": "root",
                    "attribute_code": "name"
                }],
                "matrix_code": "group"
            }]
        }
    }
}


DEFAULT_MATRIX = [
    {
        "attribute_name": "名称",
        "attribute_code": "name",
        "value": "",
        "front_type": 'singleRowText',
        "max_value": 200,
        "min_value": 0,
        "min_length": 0,
        "required": True,
        "precision": 0,
        "regexp": "",
        "max_length": 200,
        "unit": "",
        "options": [{'name': '', 'code': '', 'checked': False}]
    }
]
