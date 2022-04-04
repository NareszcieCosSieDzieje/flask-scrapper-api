# import sys
# sys.path.insert(1, "..") # FIXME
from flask import Flask, request, jsonify
from flask_apscheduler import APScheduler
from flask_mail import Mail, Message
from scrapping.scrapper import SmogScrapper, GovScrapper, SmogMapScrapper
from models.schema import Smog, Email, sqlite_db  # FIXME
from peewee import SqliteDatabase  # FIXME?
# from flask_sqlalchemy import SQLAlchemy # FIXME WYWAL
from pathlib import Path

# TODO: INITIALIZE DB

scrappers = (GovScrapper(), SmogMapScrapper(), )

# set configuration values


class Config:
    SCHEDULER_API_ENABLED = True

# app.config['MAIL_SERVER']='smtp.mailtrap.io'
# app.config['MAIL_PORT'] = 2525
# app.config['MAIL_USERNAME'] = '97e041d5e367c7'
# app.config['MAIL_PASSWORD'] = 'cfaf5b99f8bafb'
# app.config['MAIL_USE_TLS'] = True
# app.config['MAIL_USE_SSL'] = False
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db' # FIXME


app = Flask(__name__)
app.config.from_object(Config())
mail = Mail(app)

# db = SQLAlchemy(app)

smog_db_path: Path = Path(__file__).parent / "database" / "smog.db"

if app.config['DEBUG']:
    database = SqliteDatabase(smog_db_path.as_uri())
elif app.config['TESTING']:
    database = SqliteDatabase(':memory:')

database = SqliteDatabase(':memory:')  # FIXME
sqlite_db.initialize(database)
database.create_tables([Email, Smog])
Email.insert_many(["elo@gmail.com", "blabla@wp.pl"])

# Configure our proxy to use the db we specified in config.

scheduler: APScheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()


@app.route("/")
def hello():
    return "Hello World!"


@app.route('/smog/')
@app.route('/smog/<int:id>', methods=['GET'])  # TODO: PO ID CZY STRING, to i to??
def query_smog(id: int = None):
    result = None
    if id:
        result: Smog = dict(Smog.select().where(Smog.id == id))
    else:
        result: list[Smog] = [dict(smog) for smog in Smog.select()]
    return jsonify(result)


@app.route('/emails/')
@app.route('/emails/<int:id>', methods=['GET'])
def query_emails(id: int = None):
    # name = request.args.get('name')
    result = None
    if id:
        result: Email = dict(Email.select().where(Email.id == id))
    else:
        result: list[Email] = [dict(email) for email in Email.select()]
    return jsonify(result)

# @app.route('/', methods=['POST'])
# @app.route('/', methods=['DELETE'])
# @app.route('/', methods=['PUT'])


def send_mail(destination: str):
    # CREATE AN ACCOUNT? CZY KOLEJKCA ACCOUNTS
    msg = Message('Hello from the other side!', sender = 'peter@mailtrap.io', recipients = ['paul@mailtrap.io'])
    msg.body = "Hey Paul, sending you this email from my Flask app, lmk if it works"
    mail.send(msg)


@scheduler.task('cron', id='Periodically perform web-scrapping to get SMOG data', hour="6-8,18-20") # TODO: PARAMETRIZE
# @scheduler.task('cron', id='Periodically perform web-scrapping to get SMOG data', second="*") # TODO: PARAMETRIZE
# def scheduled_smog_scrapping(scrappers: list[SmogScrapper]):
def scheduled_smog_scrapping():
    for scrapper in scrappers:
        parsed_smog_list: list[Smog] = scrapper.parse_urls()
        print(parsed_smog_list)
        # print([vars(x) for x in parsed_smog_list if x is not None])
    # UPDATE DB
    # GET UPDATES!
    # IF LEVELS ARE CRITICAL SEND EMAIL


def main() -> None:
    app.run()


if __name__ == "__main__":
    main()

# run cyclically
# send email if levels are a real piece of shite
# get statistics
