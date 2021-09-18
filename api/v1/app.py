#!/usr/bin/python3
'''
   contain teardown method
'''
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from flask_cors import CORS
import os


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["0.0.0.0"]}})

app.register_blueprint(app_views)


@app.errorhandler(404)
def handle_404(error):
    ''' custom JSON 404 error'''
    return (jsonify({"error": "Not found"}), 404)


@app.teardown_appcontext
def teardown(exception):
    '''
        Teardown method for storage session
    '''
    storage.close()


if __name__ == "__main__":
    app_host = os.getenv('HBNB_API_HOST')
    app_port = os.getenv('HBNB_API_PORT')
    if app_host is None:
        app_host = '0.0.0.0'
    if app_port is None:
        app_port = 5000
    app.run(host=app_host, port=int(app_port))
