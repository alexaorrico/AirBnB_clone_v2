#!/usr/bin/python3
'''api entry point'''
from api.v1.views import app_views
from flask import Flask, jsonify, make_response
from flask_cors import CORS
from models import storage
import os


app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app, origins='0.0.0.0')
app.register_blueprint(app_views)
HBNB_API_HOST = os.getenv('HBNB_API_HOST', '0.0.0.0')
HBNB_API_PORT = int(os.getenv('HBNB_API_PORT', '5000'))


@app.teardown_appcontext
def teardown(self):
    '''close query after each session'''
    storage.close()


@app.errorhandler(404)
def not_found(error):
    '''404 error handler'''
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    app.run(host=HBNB_API_HOST, port=HBNB_API_PORT, threaded=True)
