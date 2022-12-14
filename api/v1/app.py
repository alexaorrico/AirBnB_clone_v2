#!/usr/bin/python3
""" set up """

from flask import Flask, request
from models import storage
from api.v1.views import app_views
from os import getenv, environ

app = Flask(__name__)
app.register_blueprint(app_views)

@app.teardown_appcontext
def close():
    """ method that closes a sesion """
    storage.close()

if __name__ == "__main__":
    """ rinnung a server """
    if getenv('HBNB_API_HOST') == None:
        environ['HBNB_API_HOST'] = '0.0.0.0'
    if getenv('HBNB_API_PORT') == None:
        environ['HBNB_API_PORT'] = 5000

    app.run(host=getenv('HBNB_API_HOST'),
            port=getenv('HBNB_API_PORT'),
            threaded=True, debug=True)
