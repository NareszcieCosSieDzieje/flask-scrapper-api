import logging
from logging_setup.init_logging import setup_logging
setup_logging()  # FIXME? here or after imports?

logger: logging.Logger = logging.getLogger(__name__)

from flask import Flask, request, jsonify, Response
from flask_apscheduler import APScheduler
from flask_mail import Mail, Message
from peewee import SqliteDatabase  # FIXME?
from pathlib import Path
from typing import Any
import dramatiq

from scrapping.scrapper import SmogScrapper, GovScrapper, SmogMapScrapper
from models.schema import (
    sqlite_db,
    Email,
    Smog,
    smog_factory
)
from config import (
    FlaskConfig,
    # FIXME!
)
from routes import (
    email_api,
    smog_api,
    open_api,
)
import tasks

# FIXME WYNIKI!
# redis_broker = RedisBroker(host="redis")
# results_backend = RedisBackend(host="redis")
# redis_broker.add_middleware(Results(backend=results_backend))
# dramatiq.set_broker(redis_broker)

# redis_broker: RedisBroker = RedisBroker(host="redis")  # FIXME ADD!
# dramatiq.set_broker(redis_broker)

app: Flask = Flask(__name__)
app.config.from_object(FlaskConfig())

app.register_blueprint(email_api, url_prefix='/emails')  # FIXME IS THE PREFIX NECESSARY?
app.register_blueprint(smog_api, url_prefix='/smog')
app.register_blueprint(open_api, url_prefix='/')


mail: Mail = Mail(app)
scheduler: APScheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

smog_db_path: Path = Path(__file__).parent.parent / "database" / "smog.db"
# database: SqliteDatabase = SqliteDatabase(smog_db_path.as_uri())  # FIXME
# , pragmas={
    # 'journal_mode': 'wal',
    # 'cache_size': -1024 * 64})

# Configure our proxy to use the db we specified in the config.
database: SqliteDatabase | None = None
if app.config['DEBUG']:
    database = SqliteDatabase(':memory:')
else:
    database = SqliteDatabase(str(smog_db_path))
sqlite_db.initialize(database)
database.create_tables([Email, Smog])

# Email.insert_many(["elo@gmail.com", "blabla@wp.pl"])  # FIXME


@scheduler.task('cron', id='Periodically perform web-scrapping to get SMOG data', hour="6-8,18-20") # TODO: PARAMETRIZE  # FIXME UNCOMMENT
# @scheduler.task('cron', id='Periodically perform web-scrapping to get SMOG data', second="*") # TODO: PARAMETRIZE
def schedule_scrapping(): # todo: make async?
    msg = tasks.do_smog_scrapping.send()  # FIXME RET VALUE?
    try:
        result = msg.get_result(block=False)
    except dramatiq.results.errors.ResultMissing:
        print("Result is not ready yet...")
        result = msg.get_result(block=True)
        print(f"Result is {result}")

# def send_mail(destination: str):
#     # CREATE AN ACCOUNT? CZY KOLEJKCA ACCOUNTS
#     msg = Message('Hello from the other side!', sender = 'peter@mailtrap.io', recipients = ['paul@mailtrap.io'])
#     msg.body = "Hey Paul, sending you this email from my Flask app, lmk if it works"
#     mail.send(msg)
    # GET UPDATES!
    # TODO: IF LEVELS ARE CRITICAL SEND EMAIL


def main() -> None:
    app.run(debug=True)


if __name__ == "__main__":
    import sys
    assert sys.version_info >= (3, 10), "The script requires Python 3.10+."  # FIXME REMOVE THIS?
    # print(database.get_tables())
    # import time
    # time.sleep(4)
    main()

# run cyclically
# send email if levels are a real piece of shite
# get statistics
