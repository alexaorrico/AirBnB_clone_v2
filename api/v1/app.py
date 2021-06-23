#!/usr/bin/python3
"""Building our API"""
from flask import Flask, Blueprint
from models import storage
from api.v1.views import app_views
from os import getenv


app = FLASK(__name__)
app.register_blueprint(app_views)

@app.teardown_appcontext
def teardown(context):
    """"declared method to handle app.teardown
	and calls storage.close()
    """"
    storage.close()


if __name__ == "__main__":