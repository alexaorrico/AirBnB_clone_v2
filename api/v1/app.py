#!/usr/bin/pythons
from flask import Flask
from models import storage
from api.v1.views import app_views
app.register_blueprint(app_views)
from os import getenv
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={"/*":{"origins" "0:0:0:0"}})