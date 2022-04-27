import os
import logging


class FlaskConfig:
    SECRET_KEY = os.environ.get("FLASK_SECRET_KEY", os.urandom(32))
    SCHEDULER_API_ENABLED = True
    DEBUG = True
    LOGGING_LEVEL = logging.ERROR


class FlaskProdConfig(FlaskConfig):
    FLASK_ENV = 'production'
    DEBUG = False
    TESTING = False
    LOGGING_LEVEL = logging.INFO


class FlaskDevConfig(FlaskConfig):
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = True
    LOGGING_LEVEL = logging.DEBUG


class RedisConfig:
    REDIS_URL = os.environ.get('REDIS_URL', 'redis://')
    DEBUG = False
    TESTING = False
    LOGGING_LEVEL = logging.INFO


# app.config.update(
#     TESTING=True,
#     SECRET_KEY=b'_5#y2L"F4Q8z\n\xec]/'
# )
# app.config['MAIL_SERVER']='smtp.mailtrap.io'
# app.config['MAIL_PORT'] = 2525
# app.config['MAIL_USERNAME'] = '97e041d5e367c7'
# app.config['MAIL_PASSWORD'] = 'cfaf5b99f8bafb'
# app.config['MAIL_USE_TLS'] = True
# app.config['MAIL_USE_SSL'] = False

