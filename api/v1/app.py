#!/usr/bin/python3
"""This is the doc for app module"""
from flask import Flask, make_response, jsonify
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS


# instantiate Flask app instance
app = Flask(__name__)
# register 'app_views' blueprint to app
app.register_blueprint(app_views)
# instantiate CORS instance to share resources from app
# to other web apps hosted on external domain
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown(obj):
    """teardown meth to end the db session"""
    from models import storage
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """returns a response with 404 status code and json obj data"""
    return make_response(jsonify({"error": "Not found"}), 404)


@app.errorhandler(500)
def server_err(error):
    """returns a response with 500 status code and json obj data"""
    return make_response(jsonify({"error": "Internal Server Error"}), 500)


if __name__ == "__main__":
    host = getenv('HBNB_API_HOST', default='0.0.0.0')
    port = int(getenv('HBNB_API_PORT', default='5000'))

    app.run(host=host, port=port, debug=True, threaded=True)
