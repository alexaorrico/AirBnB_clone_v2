#!/usr/bin/python3
"""
Server file for HBNB version 3
"""
from flask import Flask
from models import storage
from api.v1.views import app_views
from flask_cors import CORS


app = Flask(__name__)
CORS(app, resources={r'/api/v1/*':{"origins": "*"}})
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    storage.close()


@app.errorhandler(404)
def not_found(exception):
    return {'error': "Not found"}


if __name__ == "__main__":
    import os
    hoster = os.getenv('HBNB_API_HOST', '0.0.0.0')
    porter = os.getenv('HBNB_API_PORT', '5000')

    app.run(host=hoster, port=porter, threaded=True)
