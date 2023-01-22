#!/usr/bin/python3
'''Initializing an app instance using Flask'''
from flask import Flask, Blueprint, jsonify, make_response
from models import storage
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS


app = Flask(__name__)
app.register_blueprint(app_views)
app.url_map.strict_slashes = False
cors = CORS(app, resources={"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def close_storage(exception):
    '''Closing the database storage'''
    storage.close()


@app.errorhandler(404)
def notFound(error):
    '''Returns page not found error message'''
    e = {
        "error": "Not Found"
    }
    return make_response(jsonify({'error': "Not found"}), 404)


if __name__ == "__main__":
    host = getenv("HBNB_API_HOST", "0.0.0.0")
    port = getenv("HBNB_API_PORT", "5000")
    app.run(host=host, port=port)
