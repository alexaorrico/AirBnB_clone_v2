from flask import Flask
from flask import Blueprint
from api.v1.views.index import *
app = Flask(__name__)
app_views = Blueprint('api/v1', __name__, url_prefix='/api/v1')
