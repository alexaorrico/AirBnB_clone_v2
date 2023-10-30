#!/usr/bin/python3
"""
A Flask App that integrates with AirBnB static HTML Template
"""
from api.v1.views import app_views
from flask import Flask, jsonify
from models import storage
import os


app = Flask(__name__)

#register the blueprint app_views to Flask instance app
app.register_blueprint(app_views)

host = os.getenv('HBNB_API_HOST', '0.0.0.0')
port = os.getenv('HBNB_API_PORT', 5000)

@app.teardown_appcontext
def teardown_db(exception):
    """
    a method to handle @app.teardown_appcontext that calls storage.close()
    """
    storage.close()

@app.errorhandler(404)
def not_found(error):
    """
    a method to handle page not found error
    """
    return jsonify({'error': 'Not found'}), 404

if __name__ == "__main__":
    """
    MAIN Flask App starter
    """
    # start Flask app
    app.run(host=host, port=port, threaded=True))
