from api.models.base import BasicDocument
from api.models.mould import Mould
from api.utils.common.extentions import db


class Instance(BasicDocument):
    '''
    实例
    '''
    mould = db.ReferenceField(Mould, require=True, help_text='对应的mould')
    abilities = db.DictField(require=True, help_text='属性值')
    parent = db.ReferenceField('Instance', default=None, help_text='父级实例')
    layer_id = db.StringField(max_length=255, help_text='层级ID,目前层分为资源层和应用层')
    bridges = db.ListField(db.ReferenceField('Instance'), help_text='链接实例')
    deleted_at = db.DateTimeField(default=None)

    @property
    def has_children(self):
        return len(self.children) > 0

    @property
    def children(self):
        return Instance.fetch_all(parent=self)

    @classmethod
    def get_ancestors(cls, layer_id):
        return cls.fetch_all(layer_id=layer_id, parent=None)

    @classmethod
    def update_or_create(cls, mould, abilities):
        from api.models import ChangeLog
        instance = cls.fetch_one(mould=mould, abilities__id=abilities.get('id'))
        if instance and abilities.get('id'):
            if instance.abilities != abilities:
                instance.update(abilities=abilities)
                ChangeLog.create(
                    target_type=cls.__name__,
                    target_id=instance.id,
                    before_data=instance.abilities,
                    after_data=abilities
                )
        else:
            cls.create(mould=mould, abilities=abilities)
