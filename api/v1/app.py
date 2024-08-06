#!/usr/bin/python3
""" runs main app for AirBnb RESTAPI """
from models import storage
from .views import app_views
from flask import Flask
from os import getenv
from flask import jsonify, make_response


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_app(obj):
    """ closes the application """
    storage.close()


@app.errorhandler(404)
def not_found(e):
    """ handles 404 errors """
    e = {"error": "Not found"}

    return make_response(jsonify(e), 404)


if __name__ == "__main__":
    host = getenv("HBNB_API_HOST", '0.0.0.0')
    port = getenv("HBNB_API_PORT", '5000')
    app.run(host=host, port=port, debug=True, threaded=True)
