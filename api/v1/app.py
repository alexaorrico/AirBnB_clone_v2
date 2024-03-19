#!/usr/bin/python3
"""starts a Flask web application"""
from flask import Flask, jsonify, make_response
from flask_cors import CORS
from models import storage
from api.v1.views import app_views
import os

app = Flask(__name__)


app.register_blueprint(app_views)

cors = CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def close(self):
    """closes session"""
    storage.close()


@app.errorhandler(404)
def error_message(error):
    """error message"""
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    app.run(
            host=os.getenv("HBNB_API_HOST", '0.0.0.0'),
            port=os.getenv("HBNB_API_PORT",5000),
            threaded=True,
            debug=True
            )
