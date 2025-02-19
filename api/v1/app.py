#!/usr/bin/python3
""" The main instance
of the application
"""
from flask import Flask, jsonify, make_response
from models import storage
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_appcontext(err):
    """ tear down app context """
    storage.close()


@app.errorhandler(404)
def notfound(error):
    """ return a json response of not found """
    data = {"error": "Not found"}
    resp = jsonify(data)
    return make_response(resp, 404)


if __name__ == '__main__':
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = getenv('HBNB_API_PORT', '5000')
    app.run(threaded=True, host=host, port=port)
