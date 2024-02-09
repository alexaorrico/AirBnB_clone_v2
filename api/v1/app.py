#!/usr/bin/python3
'''api main app run
This module initializes and runs the Flask application for the API.
'''


from flask import Flask, jsonify, make_response
from models import storage
from api.v1.views import app_views
from flask_cors import CORS
import os

app = Flask(__name__)
app.register_blueprint(app_views)

# Enable CORS for all routes
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown(self):
    '''Closes the database connection after each request.'''
    storage.close()


@app.errorhandler(404)
def er_404(error):
    '''Handles 404 errors by returning a JSON response.
    Returns:
        A JSON response containng Not found 404 error.
    '''
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == '__main__':
    host = os.environ.get('HBNB_API_HOST', '0.0.0.0')
    port = os.environ.get('HBNB_API_PORT', 5000)
    app.run(host=host, port=int(port), threaded=True, debug=1)
