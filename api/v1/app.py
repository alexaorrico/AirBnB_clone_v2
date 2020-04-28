#!/usr/bin/python3
""" Starts a Flash Web Application """
from models import storage
from flask import Flask
from api.v1.views import app_views
from os import getenv
from json import dumps

app = Flask(__name__)
app.register_blueprint(app_views)


@app.errorhandler(404)
def error_404(error):
    """handler for 404 errors that returns a JSON-formatted"""
    error_dict = {"error": "Not found"}
    error_dict = dumps(error_dict, indent=4)
    return error_dict, 404


@app.teardown_appcontext
def teardown_db(exception):
    """closes the storage on teardown"""
    storage.close()

if __name__ == '__main__':
    app.run(host=getenv('HBNB_API_HOST', '0.0.0.0'),
            port=int(getenv('HBNB_API_PORT', '5000')), threaded=True)
