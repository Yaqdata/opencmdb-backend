from api.models.base import BasicDocument
from api.models.mould import Mould
from api.utils.common.extentions import db


class Instance(BasicDocument):
    mould = db.ReferenceField(Mould, require=True)
    abilities = db.DictField(require=True)
    parent = db.ReferenceField('Instance', default=None)
    layer_id = db.StringField(max_length=255)

    @property
    def has_children(self):
        return len(self.children) > 0

    @property
    def children(self):
        return Instance.fetch_all(parent=self)

    @classmethod
    def get_ancestors(cls, layer_id):
        return cls.fetch_all(layer_id=layer_id, parent=None)
