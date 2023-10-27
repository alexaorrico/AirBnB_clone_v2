#!/usr/bin/python3
from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv
app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close(exception):
    """
    The function `close` is used to close a storage
    object and handle any exceptions that may occur.
    """
    storage.close()


if __name__ == '__main__':
    app.run(host=getenv("HBNB_API_HOST"),
            port=getenv("HBNB_API_PORT"), threaded=True)
