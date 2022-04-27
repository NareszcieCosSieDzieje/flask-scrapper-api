from flask import Blueprint


open_api: Blueprint = Blueprint('open_api', __name__)


@open_api.route("/")
def openapi():
    # FIXME ADD OPEN API SWAGGER SUPPORT
    return "Hello World!"
