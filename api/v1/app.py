#!/usr/bin/python3

from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(exception=None):
    """
    teardown_appcontext closes the app
    """
    storage.close()


@app.errorhandler(404)
def errot_notfound(message):
    """
    404 error
    """
    respuesta = jsonify({"error": "Not found"})
    respuesta.status_code = 404
    return respuesta


if __name__ == '__main__':
    app.run(host=getenv("HBNB_API_HOST"),
            threaded=True)
