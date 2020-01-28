#!/usr/bin/python3
"""
 Start Flask Application
"""
from models import storage
from flask import Flask, Blueprint
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def finish(NaN):
    storage.close()


if __name__ == '__main__':
    host = getenv("HBNB_API_HOST", '0.0.0.0')
    port = getenv("BNB_API_PORT", '5000')
    app.run(host=host, port=port, threaded=True)

