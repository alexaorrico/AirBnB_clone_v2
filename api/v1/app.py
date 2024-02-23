#!/usr/bin/python3

import os
from flask import Flask
from models import storage
from api.v1.views import app_views
from flask_cors import CORS


app = Flask(__name__)
cors = CORS(app)


@app.teardown_appcontext
def teardown(exception):
    """ Teardown  function """
    storage.close()

if __name__ == "__main__":
    host = "0.0.0.0"
    port = 5000
    if 'HBNB_API_HOST' in os.environ:
        host = os.environ["HBNB_API_HOST"]
    if "HBNB_API_PORT" in os.environ:
        port = int(os.environ["HBNB_API_PORT"])
    app.register_blueprint(app_views)
    app.run(host=host, port=port, threaded=True)
