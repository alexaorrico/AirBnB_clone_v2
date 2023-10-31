#!/usr/bin/python3
"""app"""
from flask import Flask, make_response, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})

app.url_map.strict_slashes = False
app.register_blueprint(app_views)

@app.teardown_appcontext
def close_storage(self):
    '''Closes the storage engine'''
    storage.close()

if __name__ == '__main__':
    api_host = getenv("HBNB_API_HOST", '0.0.0.0')
    api_port = int(getenv("HBNB_API_PORT", 5000))
    app.run(host=api_host, port=api_port, threaded=True)
