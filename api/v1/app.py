#!/usr/bin/python3
from flask import Flask, Blueprint
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close(c):
    storage.close()


if __name__ == "__main__":
    if getenv('HBNB_API_HOST') == None:
        host = "0.0.0.0"
    else:
        host = getenv('HBNB_API_HOST')

    if getenv('HBNB_API_PORT') == None:
        port = "5000"
    else:
        port = getenv('HBNB_API_PORT')
        app.run(host=host, port=port, threaded=True, debug=True)
