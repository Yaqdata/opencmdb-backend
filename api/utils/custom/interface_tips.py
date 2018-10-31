from enum import Enum


class InterfaceTips(Enum):
    # [10000: 10100)
    INVALID_REQUEST = (400, 10000, '不合法的请求')
    INVALID_TOKEN = (401, 10001, '无效的token')

    # [10100: 10200)
    DATA_NOT_EXISTED = (404, 10100, '数据不存在')
    USER_NOT_EXISTED_OR_WRONG_PASSWORD = (401, 10101, '用户名/密码错误')
    RECORD_HAS_EXISTED = (422, 10102, '记录已经存在')
    NO_PARAMS = (422, 10103, '参数不能为空')
    PARENT_DATA_NOT_EXISTED = (422, 10104, '父节点不存在')
    AGGREGATION_NOT_EXISTED = (422, 10105, '模型组不存在')
    PARENT_INSTANCE_NO_FOUND = (422, 10106, '父模型不存在')
    PARENT_ID_IS_REQUIRED = (422, 10107, 'parent_id参数是必须')
    INVALID_LAYER_ID = (404, 10108, 'layer_id不存在')
