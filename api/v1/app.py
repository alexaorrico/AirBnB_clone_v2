#!/usr/bin/python3
"""App module"""
from os import getenv
from models import storage
from api.v1.views import app_views
from flask import Flask, jsonify
from flask_cors import CORS


app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(exception):
    """closes the storage on teardown"""
    storage.close()


@app.errorhandler(404)
def handle_exception(e):
    """Handle page not found"""
    return jsonify({'error': 'Not found'}), 404


if __name__ == '__main__':
    db_host = getenv('HBNB_API_HOST', default='0.0.0.0')
    db_port = getenv('HBNB_API_PORT', default='5000')
    app.run(host=db_host, port=db_port, threaded=True)
