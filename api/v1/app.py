#!/usr/bin/python3
""" set up """

from flask import Flask, request
from models import storage
from api.v1.views import app_views
from os import getenv
from flask_cors  import CORS

app = Flask(__name__)
CORS(app)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close():
    """ method that closes a sesion """
    storage.close()


if __name__ == "__main__":
    """ rinnung a server """
    app.run(host=getenv('HBNB_API_HOST', "0.0.0.0"),
            port=getenv('HBNB_API_PORT', 5000),
            threaded=True, debug=True)
