from api.config.default import Config


class DevelopmentConfig(Config):
    DEBUG = True
    SECRET_KEY = 'opencmdb'

    # security
    SECURITY_PASSWORD_HASH = 'bcrypt'
    SECURITY_PASSWORD_SALT = 'opencmdb'

    # mongodb
    MONGODB_DB = 'opencmdb'
    MONGODB_HOST = '127.0.0.1'
    MONGODB_PORT = 27017
    MONGODB_USER = 'opencmdb'
    MONGODB_PASSWORD = 'opencmdb'

    LOG_REQUEST_ID_GENERATE_IF_NOT_FOUND = 'request_id'
    LOG_REQUEST_ID_LOG_ALL_REQUESTS = True
    LOG_REQUEST_ID_G_OBJECT_ATTRIBUTE = 'request_id'
