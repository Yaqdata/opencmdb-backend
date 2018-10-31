from flask_security import MongoEngineUserDatastore
from flask_security.utils import hash_password

from api.models import User, Role
from api.utils.common.extentions import db

user_data_store = MongoEngineUserDatastore(db, User, Role)


def create_user(email, password):
    user = user_data_store.create_user(email=email, password=hash_password(password))
    return user


def create_role(name, description):
    role = user_data_store.create_role(name=name, description=description)
    return role


def grant_role_to_user(user, role):
    user_data_store.add_role_to_user(user, role)


def init_user_info():
    user = create_user('opencmdb@devopsedu.com', 'opencmdb')
    role = create_role('admin', '管理员')
    grant_role_to_user(user, role)
