#!/usr/bin/python3
'''task 4'''

from flask import Flask, Blueprint
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)

app.register_blueprint(app_views)

@app.tearddown_appcontext
def tearitup():
    """turrupboii"""
    storage.close()

if __name__ == '__main__':
    app.run(host=getenv('HBNB_API_HOST'),
            port=getenv('HBNB_API_PORT'))
