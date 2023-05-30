#!/usr/bin/python3
"""
Flask App
"""
import os
from flask import Flask, jsonify
from api.v1.views import app_views
from models import storage
from flask_cors import CORS

""" Flask App """
app = Flask(__name__)

# strict slashes
app.url_map.strict_slashes = False

# environment
host = os.getenv('HBNB_API_HOST', '0.0.0.0')
port = os.getenv('HBNB_API_PORT', 5000)

# app_views blueprint
app.register_blueprint(app_views)

cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})

# close storage after rendering
@app.teardown_appcontext
def teardown_db(expection):
    """
    after close db
    """
    storage.close()

@app.errorhandler(404)
def not_found(error):
    """ 404 response"""
    return jsonify({'error': 'Not found'}), 404

if __name__ == "__main__":
    """ MAIN """
    app.run(host=host, port=port, threaded=True)
