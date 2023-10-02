#!/usr/bin/python3

from api.v1.views import app_views
from flask import Flask
from models import storage
import os


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext()
def teardown_appcontext(exception):
    """
    This function is a Flask decorator that is used to register a function 
    to be called when the application context is torn down.
    """
    storage.close()


if __name__ == "__main__":
    host = os.environ.get('HBNB_API_HOST')
    port = os.environ.get('HBNB_API_PORT')
    if not host:
        host = '0.0.0.0'
    if not port:
        port = '5000'
    app.run(host=host, port=port, threaded=True)
