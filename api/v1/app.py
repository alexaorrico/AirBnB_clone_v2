#!/usr/bin/python3
"""API setup
"""
from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)

app.register_blueprint(app_views)


@app.teardown_appcontext
def end_session(exception):
    """Calls on storage.close method
    """
    return storage.close()


if __name__ == "__main__":
    HOST = getenv('HBNB_API_HOST', default='0.0.0.0')
    PORT = getenv('HBNB_API_PORT', default=5000)
    app.run(host=HOST, port=PORT, threaded=True)
