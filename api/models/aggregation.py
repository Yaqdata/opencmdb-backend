from api.models.base import BasicDocument
from api.utils.common.extentions import db


class Aggregation(BasicDocument):
    '''
    模型组
    '''
    code = db.StringField(max_length=255, auto_index=True, unique=True)
    name = db.StringField(max_length=255, unique=True)
    layer_id = db.StringField(max_length=255, help_text='层级ID,目前层分为资源层和应用层')
    description = db.StringField(max_length=255, default='')

    @classmethod
    def get_aggregation_by_code(cls, code):
        return cls.fetch_one(code=code)
