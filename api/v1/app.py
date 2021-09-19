#!/usr/bin/python3
'''
   contain teardown method
'''
from flask import Flask, make_response, jsonify
from models import storage
from api.v1.views import app_views
from flask_cors import CORS
import os


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/*": {"origins": ["0.0.0.0"]}})

@app.errorhandler(404)
def not_found(error):
    """Error 404"""
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.teardown_appcontext
def teardown(exception):
    '''
        Teardown method for storage session
    '''
    storage.close()


if __name__ == "__main__":
    app_host = os.getenv("HBNB_API_HOST", default="0.0.0.0")
    app_port = os.getenv("HBNB_API_PORT", default=5000)
    app.run(host=app_host, port=int(app_port))
