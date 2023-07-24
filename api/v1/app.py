#!/usr/bin/python3
""" Returns the status of the API """
from api.v1.views import app_views
from flask import Flask, render_template
from flask import jsonify
from models import storage
from os import environ

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(exception):
    """ Close the database """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """Make of the erroro 404, not found"""
    return jsonify(error="Not found"), 404


if __name__ == "__main__":
    if "HBNB_API_HOST" in environ:
        host = environ["HBNB_API_HOST"]
    else:
        host = "0.0.0.0"
    if "HBNB_API_PORT" in environ:
        port = environ["HBNB_API_PORT"]
    else:
        port = "5000"
    app.run(host=host, port=port, threaded=True)
