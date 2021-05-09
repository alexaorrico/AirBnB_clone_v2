#!/usr/bin/python3
"""app.py"""
from models import storage
from api.v1.views import app_views
from werkzeug.exceptions import HTTPException
from flask import Flask
from os import getenv
from flask_cors import CORS
app = Flask(__name__)
CORS(app, resources={"/*": {"origins": '0.0.0.0'}})
app.register_blueprint(app_views)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


@app.teardown_appcontext
def teardown_appcontext(e):
    """teardown_appcontext"""
    storage.close()


if __name__ == "__main__":
    host = getenv('HBNB_API_HOST')
    port = getenv('HBNB_API_PORT')
    if not host:
        host = '0.0.0.0'
    if not port:
        port = '5000'
    app.run(host=host, port=port, threaded=True)
