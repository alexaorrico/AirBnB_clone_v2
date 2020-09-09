#!/usr/bin/python3
"""API Status"""
from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def CloseSession(self):
    """Close session"""
    storage.close()

if __name__ == "__main__":
    if getenv('HBNB_API_HOST') and getenv('HBNB_API_PORT'):
        host_host = getenv('HBNB_API_HOST')
        port_port = getenv('HBNB_API_PORT')
    else:
        host_host = '0.0.0.0'
        port_port = 5000
    app.run(host=getenv('HBNB_API_HOST', '0.0.0.0'),
            port=int(getenv('HBNB_API_PORT', 5000)), threaded=True)
