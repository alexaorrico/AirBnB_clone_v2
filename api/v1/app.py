#!/usr/bin/python3
'''Flask application for the AirBnB clone v3 API.'''

import os
from flask import Flask, jsonify
from flask_cors import CORS
from models import storage
from api.v1.views import app_views  

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

@app.teardown_appcontext
def teardown_db(exception):
    '''Teardown database session.'''
    storage.close()

@app.errorhandler(404)
def page_not_found(e):
    '''Custom 404 page.'''
    return jsonify(error="Not found"), 404

if __name__ == '__main__':
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = os.getenv('HBNB_API_PORT', '5000')
    app.run(host=host, port=port, threaded=True)
