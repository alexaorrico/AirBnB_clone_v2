#!/usr/bin/python3
"""starts a Flask web application"""

from models import storage
from api.v1.views import app_views
from flask import Flask
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)
hst = getenv("HBNB_API_HOST") or '0.0.0.0'
prt = getenv("HBNB_API_PORT") or '5000'


@app.teardown_appcontext
def session_off(self):
    """Shuts down app"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    return ({"error": "Not Found"})


if __name__ == "__main__":
    app.run(host=hst, port=prt, threaded=True)
