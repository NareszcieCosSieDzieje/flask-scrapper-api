from .email_api import *
from .smog_api import *
from .open_api import *
from flask import Blueprint

routes: Blueprint = Blueprint('routes', __name__)
