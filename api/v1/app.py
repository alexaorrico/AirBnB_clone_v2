#!/usr/bin/python3
"""creating a flask application"""

import os
from flask import Flask
from models import storage
from api.v1.views import app_views
from flask_cors import CORS

# create a variable app, instance of Flask
app = Flask(__name__)

# register the blueprint app_views to your Flask instance app
app.register_blueprint(app_views)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})

# declare a method to handle @app.teardown_appcontext that calls storage.close()
@app.teardown_appcontext
def teardown_db(exception):
    """Close Storage"""
    storage.close()

@app.errorhandler(404)
def not_found(error):
    """Handles Not found errors"""
    return make_response(jsonify({'error': "Not found"}), 404)

if __name__ == '__main__':
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', 5000))
    # getenv returns a string and port is an int
    # THREADED is set to true so it can serve multiple requests at once
    app.run(host=host, port=port, threaded=True)
