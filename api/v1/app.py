#!/usr/bin/python3
"""creating a flask application"""

from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS
# Create a Flask application instance
app = Flask(__name__)

app.register_blueprint(app_views)

# Register the blueprint app_views
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

# Initialize CORS with the app instance
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


# Declare a method to handle teardown
@app.teardown_appcontext
def teardown(error):
    """Clean-up method"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """Custom 404 error"""
    return jsonify({'error': 'Not found'}), 404


if __name__ == '__main__':
    app.run(host=getenv('HBNB_API_HOST'),
            port=getenv('HBNB_API_PORT'),
            threaded=True)
