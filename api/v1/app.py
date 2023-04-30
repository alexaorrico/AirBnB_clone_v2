#!/usr/bin/python3
"""
Instance of Flask app
"""
from os import getenv
from flask import Flask
from models import storage
from api.v1.views import app_views


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_storage(err):
    """ closes the storage """
    storage.close()


if __name__ == '__main__':
    myhost = getenv('HBNB_API_HOST', default="0.0.0.0")
    myport = getenv('HBNB_API_PORT', default="5000")
    app.run(threaded=True, host=myhost, port=myport)
