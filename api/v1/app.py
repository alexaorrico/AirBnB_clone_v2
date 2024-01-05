#!/usr/bin/python3

"""
setting up flask application for from
Airbnb_v3 api
"""
from api.v1.views import app_views
from flask import Flask
from models import storage
import os


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def tear_down(exception=None):
    """close session"""
    storage.close()


if __name__ == '__main__':
    host = os.environ.get('HBNB_API_HOST', '0.0.0.0')
    port = int(os.environ.get('HBNB_API_PORT', 5000))

    app.run(host=host, port=port, debug=True, threaded=True)
