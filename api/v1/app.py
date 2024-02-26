#!/usr/bin/python3

from flask import Flask
from os import getenv
from api.v1.views import app_views
from models import storage
app = Flask(__name__)

app.register_blueprint(app_views)


@app.teardown_appcontext
def tear_down(exception):
    """calls storage.close()"""
    storage.close()


if __name__ == "__main__":
    host = getenv('HBNB_API_HOST') or '0.0.0.0'
    port = getenv('HBNB_API_PORT') or 5000
    app.run(host=host, port=port, threaded=True, debug=True)
