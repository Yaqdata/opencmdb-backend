from api.models.base import BasicDocument
from api.utils.common.extentions import db


class ChangeLog(BasicDocument):
    target_type = db.StringField(max_length=128, help_text='类名')
    target_id = db.StringField(max_length=128, help_text='实例ID')
    before_data = db.DictField()
    after_data = db.DictField()
