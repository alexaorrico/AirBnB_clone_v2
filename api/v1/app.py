#!/usr/bin/python3
import os
from flask import Flask, Blueprint, jsonify
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def tearDownDB(self):
    """removes sqlalchemy session"""
    storage.close()


@app.errorhandler(404)
def errorHandler(error):
    """returns a 404 error msg"""
    return jsonify(error='Not found'), 404


# was unsure if we had environmental variables setup yet
if __name__ == '__main__':
    if os.getenv(HBNB_API_HOST):
        hostAddress = os.getenv(HBNB_API_HOST)
    else:
        hostAddress = ('0.0.0.0')
    if os.getenv(HBNB_API_PORT):
        portAddress = os.getenv(HBNB_API_PORT)
    else:
        portAddress = '5000'

    app.run(hostAddress, portAddress, threaded=True)
    # app.run(os.getenv(HBNB_API_HOST),
    # os.getenv(HBNB_API_PORT), threaded=True)
