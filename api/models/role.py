from flask_security import UserMixin

from api.models.base import BasicDocument

from api.utils.common.extentions import db


class Role(BasicDocument, UserMixin):
    name = db.StringField(max_length=80, unique=True)
    description = db.StringField(max_length=255)
