#!/usr/bin/python3
"""It's time to start your API. Your first endpoint\
(route) will be to return the status of your API"""


from api.v1.views import ap_views
from models import storage
from flask import Flask
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close(self):
    """closes session"""
    storage.close()


if __name__ == "__main__":
    if host is None:
        host = "0.0.0.0"
    else:
        host = getenv("HBNB_API_HOST")
    if port is None:
        port = "5000"
    else:
        port = getenv("HBNB_API_HOST")
    app.run(host=host, port=port, threaded=True)
