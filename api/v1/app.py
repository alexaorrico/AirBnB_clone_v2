#!/usr/bin/python3
"""run flask server"""
from api.v1.views import app_views
from flask import Flask, Blueprint, make_response
from flask_cors import CORS
from models import storage
import os

app = Flask(__name__)
app.url_map.strict_slashes = False
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.errorhandler(404)
def page_not_found(e):
    return make_response({'error': 'Not found'}, 404)


@app.teardown_appcontext
def reset(error):
    """reload data"""
    storage.close()


if __name__ == "__main__":
    try:
        app.run(host=os.getenv('HBNB_API_HOST'),
                port=os.getenv('HBNB_API_PORT'),
                threaded=True)
    except Exception:
        app.run(host='0.0.0.0', port=5000, threaded=True)
