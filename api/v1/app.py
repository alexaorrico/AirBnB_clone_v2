#!/usr/bin/python3
"""starts a flask application"""

from flask import Flask, make_response, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown_db(exception):
    """calls storage.close"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """custom 404 response"""
    return make_response(jsonify({'error': 'Not Found'}), 404)


if __name__ == '__main__':
    HOST = getenv('HBNB_API_HOST') if getenv('HBNB_API_HOST') else '0.0.0.0'
    PORT = getenv('HBNB_API_PORT') if getenv('HBNB_API_PORT') else 5000
    app.run(host=HOST, port=int(PORT), threaded=True)
