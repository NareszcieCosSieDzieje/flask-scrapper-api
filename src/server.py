import logging
from logging_setup.init_logging import setup_logging
setup_logging()  # FIXME? here or after imports?

logger: logging.Logger = logging.getLogger(__name__)

from flask import Flask, request, jsonify, Response
from flask_apscheduler import APScheduler
from flask_mail import Mail, Message
from flask_cors import CORS
from peewee import SqliteDatabase  # FIXME?
from typing import Any

from models.schema import (
    sqlite_db,
    Email,
    Smog,
)
from config import (
    FlaskConfig,
    DatabaseConfig,
    # FIXME!
)
from routes import (
    email_api,
    smog_api,
    open_api,
)
import tasks

app: Flask = Flask(__name__)
app.config.from_object(FlaskConfig())

cors: CORS = CORS(app)

app.register_blueprint(email_api)  # TODO: ? optional # url_prefix='/emails'
app.register_blueprint(smog_api)
app.register_blueprint(open_api)


mail: Mail = Mail(app)
scheduler: APScheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

smog_db_path: str = DatabaseConfig.DB_PATH

# Configure our proxy to use the db we specified in the config.
database: SqliteDatabase | None = None
if app.config['DEBUG']:
    database = SqliteDatabase(':memory:')
else:
    database = SqliteDatabase(smog_db_path)
sqlite_db.initialize(database)
database.create_tables([Email, Smog])


@scheduler.task('cron', id='Periodically perform web-scrapping and save SMOG data', hour="6-8,18-20")
def schedule_scrapping():
    _ = tasks.do_smog_scrapping.send()

# FIXME REMOVE THIS!
@app.route('/reload_data', methods=['GET'])
def reload_data():
    from datetime import datetime
    for job in scheduler.get_jobs():
        logger.info(f"Running a job: {job}")
        job.modify(next_run_time=datetime.now())
    return Response("{}", status=200, mimetype='application/json')


# TODO: Chain a trigger event after scrapping,
# If levels are CRITICAL notify the users by email
# def send_mail(destination: str):
#   pass

def main() -> None:
    app.run(debug=True) # FIXME: change debug to a var


if __name__ == "__main__":
    import sys
    assert sys.version_info >= (3, 10), "The script requires Python 3.10+."
    main()
