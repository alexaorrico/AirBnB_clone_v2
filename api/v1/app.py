#!/usr/bin/python3
""" Your first endpoint (route) will be to return the status of your API """
from models import storage
from api.v1.views import app_views
from flask import Flask
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)

@app.teardown_appcontext
def Down_World(exception):
    """ DB will be closed automatically at the end of the request """
    storage.close()

if __name__ == "__main__":
    host = getenv('HBNB_API_HOST')
    if not host:
        host = '0.0.0.0'
    port = getenv('HBNB_API_PORT')
    if not port:
        port = '5000'

    app.run(host=host, port=port, threaded=True)
