#!/usr/bin/python3
""" Entrypoint of AIRBNB api """
import os
from flask import Flask
from models import storage
from flask import Blueprint
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)

@app.teardown_appcontext
def teardown_appcontext_func(error):
    """ Close the session """
    storage.close()

@app.errorhandler(404)
def page_not_found(e):
    """ Custon error 404 handler """
    return ('{\n  "error": "Not found"\n}\n'), 404


if __name__ == "__main__":
    host = "0.0.0.0"
    port = '5000'

    if os.getenv('HBNB_API_HOST') == "0.0.0.0":
        host = os.getenv('HBNB_API_HOST')

    if os.getenv('HBNB_API_PORT') == "5000":
        port = "5000"

    app.run(host=host, port=port, threaded=True, debug=True)
