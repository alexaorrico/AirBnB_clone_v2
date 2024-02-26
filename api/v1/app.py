#!/usr/bin/python3
"""
API
"""
from models import storage
from flask import Flask, make_response, jsonify
from . import views
from os import getenv
from flask_cors import CORS
host = getenv('HBNB_API_HOST')
port = getenv('HBNB_API_PORT')


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
# how the app will be viewed, many pages, many routes
app.register_blueprint(views.app_views)


@app.teardown_appcontext
def teardown_db(exception):
    """closes the storage on teardown"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    if port and host:
        app.run(host=host, port=port, threaded=True)
    elif port and not host:
        app.run(host='0.0.0.0', port=port, threaded=True)
    elif not port and host:
        app.run(port=5000, host=host, threaded=True)
    else:
        app.run(port=5000, host='0.0.0.0', threaded=True)
