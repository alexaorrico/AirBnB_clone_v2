#!/usr/bin/python3
"""
Contains the FileStorage class
"""
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

@app.teardown_appcontext
def teardown_db(exception):
    storage.close()

@app.errorhandler(404)
def not_found(error):
    """Returns a 404 JSON-formatted response"""
    return jsonify({'error': 'Not found'}), 404

if __name__ == "__main__":
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(getenv('HBNB_API_PORT', 5000))
    app.run(host=host, port=port, threaded=True)
