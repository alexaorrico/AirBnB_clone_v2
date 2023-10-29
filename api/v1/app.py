#!/usr/bin/python3
"""
initializing flask app
"""
from models import storage
from api.v1.views import app_views
from flask import Flask
from os import getenv
app = Flask(__name__)
app.register_blueprint(app_views)

app.do_teardown_appcontext()
def tear_down(data):
    """
    tear down app
    """
    storage.close()


if __name__ == "__main__":
    """ Main Function """
    host = getenv('HBNB_API_HOST')
    port = getenv('HBNB_API_PORT')
    if not host:
        host = '0.0.0.0'
    if not port:
        port = '5000'
    app.run(host=host, port=port, threaded=True)
