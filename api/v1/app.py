#!/usr/bin/python3
"""
Status of my API
"""
import os
from api.v1.views import app_views
from flask import Flask
from models import storage
app = Flask(__name__)


app.register_blueprint(app_views, url_prefix='/api/v1')
@app.teardown_appcontext
def tear(error):
    storage.close()


if __name__ == '__main__':
    if os.getenv('HBNB_API_HOST'):
        host = os.getenv('HBNB_API_HOST')
    else:
        host = '0.0.0.0'
    if os.getenv('HBNB_API_PORT'):
        port = os.getenv('HBNB_API_PORT')
    else:
        port = 5000
    app.run(host=host, port=port, threaded=True)
