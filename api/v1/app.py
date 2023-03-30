#!/usr/bin/python3
'''
    using variables to connect to API
'''
import os
from flask import Flask, jsonify
from flask_cors import CORS
from api.v1.views import app_views
from models import storage

app = Flask(__name__)
app.register_blueprint(app_views, url_prefix='/api/v1')
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})

host = os.environ.get('HBNB_API_HOST', '0.0.0.0')
port = os.environ.get('HBNB_API_PORT', '5000')
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


@app.teardown_appcontext
def close_storage(error):
    '''
        engage in teardowns
    '''
    storage.close()


@app.errorhandler(404)
def not_found(error):
    '''
        JSON-formatted response
    '''
    return jsonify({'error': 'Not found'}), 404


if __name__ == '__main__':
    app.run(host=host, port=port)
