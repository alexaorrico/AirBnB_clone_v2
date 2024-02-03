#!/usr/bin/python3
"""App API"""


from api.v1.views import app_views
from flask import Flask, make_response, jsonify
from os import getenv
from models import storage

app = Flask(__name__)
app.register_blueprint(app_views)

if getenv('HBNB_API_HOST'):
    HBNB_HOST = getenv('HBNB_API_HOST')
else:
    HBNB_HOST = '0.0.0.0'

if getenv('HBNB_API_HOST'):
    HBNB_PORT = getenv('HBNB_API_PORT')
else:
    HBNB_PORT = 5000


@app.teardown_appcontext
def teardown_db(exception=None):
    """Closes storage on teardown"""
    storage.close()


@app.errorhandler(404)
def notFound(err):
    """ handler error 404 """
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    """func"""
    app.run(host=HBNB_HOST, port=HBNB_PORT, debug=True)
