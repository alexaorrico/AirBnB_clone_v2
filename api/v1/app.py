#!/usr/bin/python3
"""
Script that starts a Flask web application
"""
from flask import Flask, render_template
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app_views = app

"""app.register_blueprint(app_views)
app.register_blueprint(app_views)"""

app_views = Blueprint('app_views', app)


@app.teardown_appcontext
def tear(self):
    """Method to handle tearmod"""
    storage.close()


if __name__ == "__main__":

    if getenv("HBNB_API_HOST") is None:
        HBNB_API_HOST = "0.0.0.0"

    if getenv("HBNB_API_PORT") is None:
        HBNB_API_PORT = 5000

    app.run(host=HBNB_API_HOST, port=int(
        HBNB_API_PORT), debug=True, threaded=True)
