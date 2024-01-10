#!/usr/bin/python3
"""return the status of your API
"""

from flask import Flask, make_response
from models import storage
from os import getenv
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_appcontext(exception):
    """close storage
    """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """handles a JSON-formatted 404 status code response
    """
    return make_response({"error": "Not found"}, 404)


if __name__ == "__main__":
    HBNB_API_HOST = getenv('HBNB_API_HOST')
    HBNB_API_PORT = getenv('HBNB_API_PORT')
    app.run(host=HBNB_API_HOST, port=HBNB_API_PORT, threaded=True)
