import os
import logging
from pathlib import Path
class FlaskConfig:
    SECRET_KEY = os.environ.get("FLASK_SECRET_KEY", os.urandom(32))
    SCHEDULER_API_ENABLED = True
    DEBUG = bool(int(os.environ.get("DEBUG", 0)))  # FIXME: what if not int
    FLASK_ENV = os.environ.get("FLASK_ENV", "development")
    # TESTING = os.environ.get("TESTING", "development")
    # if FLASK_ENV == "development":
    #     TESTING = True
    # LOGGING_LEVEL = logging.ERROR


class CorsConfig:
    # TODO:
    # https://flask-cors.readthedocs.io/en/latest/configuration.html
    CORS_ALLOW_HEADERS = "*"

class FlaskProdConfig(FlaskConfig):
    FLASK_ENV = "production"
    DEBUG = False
    TESTING = False
    LOGGING_LEVEL = logging.INFO


class FlaskDevConfig(FlaskConfig):
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = True
    LOGGING_LEVEL = logging.DEBUG


class RedisConfig:
    REDIS_PORT = os.environ.get('REDIS_PORT', "6379")
    REDIS_HOST = os.environ.get('REDIS_HOST', "redis")
    DB_NUM = os.environ.get('DB_NUM', "0")
    REDIS_URL = os.environ.get('REDIS_URL', f"redis://{REDIS_HOST}:{REDIS_PORT}/{DB_NUM}")


class DatabaseConfig:
    DB_PATH: str = str(Path(__file__).parent.parent / "database" / "smog.db")

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

