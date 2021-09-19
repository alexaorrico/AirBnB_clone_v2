#!/usr/bin/python3
"""
return the status of your API for AirBnB_clone
"""

import os
from flask_cors import CORS
from flask import Flask, jsonify, Response
from api.v1.views import app_views
from models import storage

app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})

@app.teardown_appcontext
def teardown(self):
    ''' to teardown the app '''
    storage.close()

@app.errorhandler(404)
def page_not_found(e):
    ''' 404 errors definition '''
    return jsonify({"error": "Not found"}), 404

if __name__ == "__main__":
    try:
        host = os.environ.get('HBNB_API_HOST')
    except:
        host = '0.0.0.0'

    try:
        port = os.environ.get('HBNB_API_PORT')
    except:
        host = '5000'

    app.run(host=host, port=port)
