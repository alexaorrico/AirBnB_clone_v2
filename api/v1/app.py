#!/usr/bin/python3
"""
    This is the script that actually starts our web app
"""
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(app_views)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.errorhandler(404)
def not_found_error(error):
    """ method for Custom 404 error
    """
    return jsonify({'error': 'Not found'}), 404


@app.teardown_appcontext
def teardown_method(error):
    """method for cleanup
    """
    storage.close()

if __name__ == '__main__':
    app.run(host=getenv('HBNB_API_HOST'),
            port=getenv('HBNB_API_PORT'),
            threaded=True)
