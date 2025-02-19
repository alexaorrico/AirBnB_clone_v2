#!/usr/bin/python3
"""
    app.py:
        a flask application that creates a REST api

"""
import os
from flask import Flask
from flask_cors import CORS
from models import storage
from api.v1.views import app_views


app = Flask(__name__)
CORS(app, origins=["0.0.0.0"])
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_hbnb_storage(exception):
    """ close sqlalchemy storage """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """ a custom json 404 eror """
    return {"error": "Not found"}, 404


if __name__ == "__main__":
    host = os.getenv('HBNB_API_HOST')
    port = os.getenv('HBNB_API_PORT')

    app.run(host=host, port=port, threaded=True)
