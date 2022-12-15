#!/usr/bin/python3
"""immported modules pa"""
from os import getenv
from api.v1.views import app_views
from models import storage
from flask import Flask

'''
if os.getenv("HBNB_API_HOST"):
    HBNB_API_HOST = os.getenv("HBNB_API_HOST")
else:
    HBNB_API_HOST = "0.0.0.0"

if os.getenv("HBNB_API_PORT"):
    HBNB_API_PORT = os.getenv("HBNB_API_PORT")
else:
    HBNB_API_PORT = 5000'''

app = Flask(__name__)
app.register_blueprint(app_views)



@app.teardown_appcontext
def close_this(self):
    """close the storage instance"""
    storage.close()


if __name__ == "__main__":
    """documented pa"""

    hostapi = getenv('HBNB_API_HOST', default='0.0.0.0')
    portapi = getenv('HBNB_API_PORT', default=5000)
    app.run(host=hostapi, port=portapi, threaded=True)    hostapi = getenv('HBNB_API_HOST', default='0.0.0.0')
    portapi = getenv('HBNB_API_PORT', default=5000)
    app.run(host=hostapi, port=portapi, threaded=True)