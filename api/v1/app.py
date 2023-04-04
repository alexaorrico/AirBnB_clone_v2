#!/usr/bin/python3
""" starting the Flash """
from api.v1.views import app_views
from flask import Flask, jsonify, make_response
from flask_cors import CORS
from models import storage
from os import environ


# instance of flask
app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views)


@app.errorhandler(404)
def not_found(error):
    """ 404(page not found) """
    return make_response(jsonify({"error": "Not found"}), 404)


@app.teardown_appcontext
def close_storage(exception=None):
    """ Close Storage """
    storage.close()


if __name__ == '__main__':
    host = environ.get("HBNB_API_HOST", "0.0.0.0")
    port = environ.get("HBNB_API_PORT", 5000)
    app.run(host=host, port=port, threaded=True)
