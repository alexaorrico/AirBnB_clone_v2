#!/usr/bin/python3
"""Flask Api Module"""
from api.v1.views import app_views
from flask import Flask, jsonify, make_response
from models import storage
from os import getenv


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(self):
    """teardown"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """ returns a JSON-formatted 404 status code response """
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == '__main__':
    HOST = getenv('HBNB_API_HOST', '0.0.0.0')
    PORT = getenv('HBNB_API_PORT', 5000)
    app.run(host=HOST, port=PORT, threaded=True)
