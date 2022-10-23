#!/usr/bin/python3
'''first endpoint (route) to return the status of your API'''

import code
from flask import Flask
from models import storage
from api.v1.views import app_views
from flask import Blueprint
import os

app = Flask(__name__)
app.register_blueprint(app_views)
@app.teardown_appcontext
def closestorage(code):
    '''teardown context'''
    storage.close()


if __name__ == "__main__":
    app.run(host=os.getenv("HBNB_API_HOST", '0.0.0.0'),
            port=os.getenv('HBNB_API_PORT', '5000'), threaded=True)
