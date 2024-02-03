#!/usr/bin/python3
''' Status of your API '''
from api.v1.views import app_views
from flask import Flask, jsonify
import os
from flask_cors import CORS
from models import storage

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(exception):
    """closes the storage on teardown"""
    storage.close()


@app.errorhandler(404)
def handle_bad_request(e):
    response = {"error": "Not found"}
    return jsonify(response), 404


if __name__ == '__main__':
    if 'HBNB_API_HOST' in os.environ and 'HBNB_API_PORT' in os.environ:
        app.run(host=os.environ['HBNB_API_HOST'],
                port=os.environ['HBNB_API_PORT'], threaded=True)
    else:
        app.run(host='0.0.0.0', port='5000', threaded=True)
