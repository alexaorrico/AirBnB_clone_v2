#!/usr/bin/python3
"""
Starts up a copy of a flask-app
"""
from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv as env
app = Flask(__name__)

app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(self):
    """Closes the storage on teardown"""
    storage.close()


@app.errorhandler(404)
def page_not_found(e):
    """404 error handler"""
    return {"error": "Not found"}, 404


def start_flask():
    """ start flask """
    app.run(host=env('HBNB_API_HOST', default='localhost'),
            port=env('HBNB_API_PORT'),
            threaded=True)


if __name__ == "__main__":
    start_flask()
