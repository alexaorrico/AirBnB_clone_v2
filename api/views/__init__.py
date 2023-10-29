from flask import Flask
from flask import Blueprint
from api.v1.views import *





pp = Flask(__name__)
app_views = Blueprint('app_views', __name__)