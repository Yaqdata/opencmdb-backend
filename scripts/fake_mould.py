from api.models import (Aggregation, Mould)


def fake_mould():
    aggregation = Aggregation.create(
        **{
            'code': 'aggregation_1',
            'name': '主机模块'
        }
    )
    for i in range(19):
        Mould.create(
            **{
                'code': 'mould_{}'.format(i),
                'name': 'name_{}'.format(i),
                'aggregation': aggregation,
                'matrix': [{
                    'code': 'default',
                    'name': '默认信息',
                    'values': [
                        {
                            'name': '字符串',
                            'required': True,
                            'value_type': 'string'
                        }, {
                            'name': '整型',
                            'required': False,
                            'value_type': 'integer'
                        }, {
                            'name': '浮点型',
                            'required': True,
                            'value_type': 'float'
                        }, {
                            'name': '富文本',
                            'required': False,
                            'value_type': 'text'
                        }
                    ]
                }]
            }
        )
