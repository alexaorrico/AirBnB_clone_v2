#!/usr/bin/python3
""" create a variable app, instance of Flask """

from flask import Flask

app = Flask(__name__)

from models import storage
from api.v1.views import app_views

app.register_blueprint(app_views)

@app.teardown_appcontext
def teardown
