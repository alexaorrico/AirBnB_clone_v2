#!/usr/bin/python3
""" Flask module, returs status of the api. """
from api.v1.views.__init__ import app_views
from flask import Flask
from models import storage
from os import getenv as env

app = Flask(__name__)
app.register_blueprint(app_views)


@app.errorhandler(404)
def page_not_found(e):
    """ Error handler"""
    return({"error": "Not found"})


@app.teardown_appcontext
def close_connection(exception):
    """ Closes the session's connection. """
    storage.close()

if __name__ == "__main__":

    host = "0.0.0.0"
    port = "5000"

    if env("HBNB_API_HOST"):
        host = env("HBNB_API_HOST")

    if env("HBNB_API_PORT"):
        port = env("HBNB_API_PORT")

    app.run(host=host, port=port, threaded=True, debug=True)
