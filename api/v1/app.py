#!/usr/bin/python3
"""
starts a Flask web application
"""

from api.v1.views import app_views
from flask import Flask
from models import storage
import os

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def tearthisdown(exception):
    '''teardown function. This close SQalchemy session'''
    storage.close()

if __name__ == "__main__":
    thishost = os.getenv('HBNB_API_HOST', '0.0.0.0')
    thisport = os.getenv('HBNB_API_PORT', 5000)
    app.run(host=thishost, port=thisport, threaded=True)
