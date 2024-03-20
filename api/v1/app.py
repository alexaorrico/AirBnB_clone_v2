#!/usr/bin/python3
""" initializes Flask application """
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
import os
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(app_views)
# Create a CORS instance and allow all domains for all routes
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def close_db(exception):
    """ closes db """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    response = jsonify({'error': 'Not found'}), 404
    return response


if __name__ == '__main__':
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', '5000'))
    app.run(debug=True, host=host, port=port, threaded=True)
