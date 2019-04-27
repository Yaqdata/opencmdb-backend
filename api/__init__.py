from flask import Flask
from flask_cors import CORS
from flask_security import MongoEngineUserDatastore
from flask_log_request_id import RequestID

from api.config import load_config
from api.utils.custom.error import error
from api.utils.custom.interface_tips import InterfaceTips
from api.models import User, Role
from api.controller.app_v0_1.view import BLUEPRINTS
from api.utils.common.extentions import (db, security)


def extensions_load(app):
    db.init_app(app)
    RequestID(app)
    user_data_store = MongoEngineUserDatastore(db, User, Role)
    s = security.init_app(app, user_data_store, register_blueprint=False)
    cors = CORS(app, resources={r"*": {"origins": "*", "expose_headers": "X-Total"}})

    # TODO 无法分辨token过期/没有token/无效的token
    def unauthorized_handler():
        error(InterfaceTips.INVALID_TOKEN)
    s.unauthorized_handler(unauthorized_handler)


def blueprints_resister(app, blueprints):
    for bp in blueprints:
        app.register_blueprint(bp)


def create_app(app_name='api', blueprints=None):
    app = Flask(app_name)
    config = load_config()
    app.config.from_object(config)

    if not blueprints:
        blueprints = BLUEPRINTS

    blueprints_resister(app, blueprints)
    extensions_load(app)
    return app



