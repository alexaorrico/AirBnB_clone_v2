#!/usr/bin/python3
# Index

from api.v1.views import app_views
from flask_api import status
from flask import jsonify


@app_views.route('/status'):
def status():
    dictionary = {}
    dictionary['status'] == "Ok"
    return json.dump(dictionary)