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
