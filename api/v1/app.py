#!/usr/bin/python3
"""main app module"""
from flask import Flask
from models import storage
from api.v1.views import app_views
from flask_cors import CORS
import os


app = Flask(__name__)
app.register_blueprint(app_views)
app.url_map.strict_slashes = False
cors = CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})

@app.teardown_appcontext
def teardown(code):
    """calls storage.close method"""
    storage.close()


@app.errorhandler(404)
def not_found(e):
    """returns 404 error"""
    return ({"error": "Not found"}), 404


if __name__ == "__main__":
    """running app"""
    app.run(host=os.getenv('HBNB_API_HOST', '0.0.0.0'),
            port=os.getenv('HBNB_API_PORT', '5000'),
            threaded=True)
