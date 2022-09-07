#!/usr/bin/python3
'''
Creating and starting API
'''

from models import storage
from api.v1.views import app_views
from flask import Flask
from flask import Blueprint
from os import getenv
from flask import jsonify

app = Flask(__name__)
app.register_blueprint(app_views)

@app.teardown_appcontext
def teardown_appcontext(self):
    '''Method to handle that calls storage.close()'''
    storage.close()

@app.errorhandler(404)
def handle_exception(e):
    return jsonify({"error": "Not found"})

if __name__ == "__main__":
    if getenv('HBNB_API_HOST') is None:
        host = '0.0.0.0'
    else:
        host = getenv('HBNB_API_HOST')

    if getenv('HBNB_API_PORT') is None:
        port = 5000
    else:
        port = getenv('HBNB_API_PORT')

    app.run(host, port, threaded=True)