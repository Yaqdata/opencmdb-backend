from api.models.base import BasicDocument
# from api.models.aggregation import Aggregation
from api.utils.common.extentions import db
from api.utils.custom.constants import DEFAULT_MATRIX


class Mould(BasicDocument):
    code = db.StringField(max_length=255, auto_index=True, unique=True)
    name = db.StringField(max_length=255, unique=True)
    aggregation = db.ReferenceField('Aggregation', require=True)
    description = db.StringField(max_length=255, default='')
    matrix = db.ListField(default=DEFAULT_MATRIX)
    layer_id = db.StringField(max_length=255)
    parent = db.ReferenceField('Mould', default=None)

    def _validate_ability(self, key, ability, d_type, required=False):
        if required and ability is None:
            return False, {key: '数据不能为空'}

        if type(ability) == d_type:
            return True, {}
        return False, {key: '数据类型不正确，需要的是{}'.format(d_type)}

    def validate_abilities(self, abilities):
        msgs = {}
        for mat in self.matrix:
            for attribute in mat.get('attributes'):
                value = abilities.get(attribute.get('attribute_code'))
                success, msg = self._validate_ability(
                    value, attribute.get('attribute_name'), attribute.get('type'), attribute.get('required', False)
                )
                if not success:
                    msgs.update(msg)

        return len(msgs) > 0, msgs

    @property
    def has_children(self):
        return len(self.children) > 0

    @property
    def children(self):
        return Mould.fetch_all(parent=self)

    @classmethod
    def get_ancestors(cls, layer_id):
        return cls.fetch_all(layer_id=layer_id, parent=None)
