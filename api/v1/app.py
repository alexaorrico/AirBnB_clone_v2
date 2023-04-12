#!/usr/bin/python3

from flask import Flask, Blueprint
from models import storage
from api.v1.views import app_view

app = Flask(__name__)
app.register_blueprint(app_view)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', threaded=True)