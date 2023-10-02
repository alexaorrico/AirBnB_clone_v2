#!/usr/bin/python3
"""app"""
import os

from flask import Flask, make_response, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS



app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})


app.url_map.strict_slashes = False

"""Register the blueprint app_views to your Flask instance app"""
app.register_blueprint(app_views)



"""Define a method to handle app teardown"""
@app.teardown_appcontext
def tear(self):
    """ closes storage engine """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """ handles 404 error and gives json formatted response """
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == "__main__":
    """Define host and port from environment variables or use default values"""
    host = os.getenv("HBNB_API_HOST", "0.0.0.0")
    port = int(os.getenv("HBNB_API_PORT", 5000))

    """Run the Flask server"""
    app.run(host=host, port=port, threaded=True)
