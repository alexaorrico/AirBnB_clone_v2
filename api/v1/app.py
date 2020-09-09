#!/usr/bin/python3
"""
Restful api Flask Module
"""
from os import getenv
from api.v1.views import app_views
from models import storage
from flask import Flask

# flask instance
app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_storage(exce):
    ''' Calls close from storage '''
    storage.close()


if __name__ == "__main__":
    app.run(
        host=getenv("HBNB_API_HOST"),
        port=getenv("HBNB_API_PORT"),
        threaded=True)
