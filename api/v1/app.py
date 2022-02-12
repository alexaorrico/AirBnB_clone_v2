#!/usr/bin/python3
""" flask app main file """
from flask import Flask, jsonify, make_response
from os import environ
from api.v1.views import app_views
from models import storage
from werkzeug.exceptions import HTTPException

HBNB_API_PORT = environ.get("HBNB_API_PORT")
HBNB_API_HOST = environ.get("HBNB_API_HOST")

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exe):
    """ closes the db connection """
    storage.close()

@app.errorhandler(404)
def notfound(exception):
    """
    handles the notfound error
    """
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    app.run(host=HBNB_API_HOST, port=HBNB_API_PORT, threaded=True)
