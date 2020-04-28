#!/usr/bin/python3
"""
Flask App that integrates with AirBnB static HTML Template
"""

from api.v1.views import app_views
from models import storage
from flask import Flask, jsonify, make_response, render_template
from flask_cors import CORS
import os

# Variable instance of flask named app
app = Flask(__name__)
# CORS app
CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})

# Flask server enviromental variables setup
host = os.getenv('HBNB_API_HOST', '0.0.0.0')
port = os.getenv('HBNB_API_PORT', 5000)

# Blueprint app_views register. (Defined in api.v1.views)
app.register_blueprint(app_views)


# Flask page rendering
@app.teardown_appcontext
def teardown_db(exception):
    """
    after each request, this method calls .close() on
    the current SQLAlchemy Session
    """
    storage.close()

@app.errorhandler(404)
def handle_404(exception):
    """
    Handler for 404 error (Not Found)
    """
    code = exception.__str__().split()[0]
    description = "Not found"
    message = {'error': description}
    return make_response(jsonify(message), code)

if __name__ == "__main__":
    """
    MAIN Flask App
    """
    # start Flask app
    app.run(host=host, port=port)
