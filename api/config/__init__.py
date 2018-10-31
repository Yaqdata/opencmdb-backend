import os


def load_config():
    mode = os.environ.get('FLASK_ENV')
    try:
        if mode == 'PRODUCTION':
            from api.config.production import ProductionConfig
            return ProductionConfig
        elif mode == 'TESTING':
            from api.config.testing import TestingConfig
            return TestingConfig
        else:
            from api.config.development import DevelopmentConfig
            return DevelopmentConfig
    except Exception as e:
        from api.config.default import Config
        return Config

