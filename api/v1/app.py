#!/usr/bin/python3
""" Api module """
from api.v1.views import app_views
from flask import Flask
from models import storage

app = Flask(__name__)

app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    """teardown"""
    storage.close()


if __name__ == "__main__":
    host = "0.0.0.0" if host is None
    port = 5000 if port is None else port
    app.run(host=host, port=port, threaded=True)
