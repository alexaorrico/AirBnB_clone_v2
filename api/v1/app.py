#!/usr/bin/python3
"""
Registers Blueprint 'app_views'
from 'api.v1.views' into this script's
app, 'app', then runs 'app'

with
-----------------------------------------
host=HBNB_API_HOST and port=HBNB_API_PORT
-----------------------------------------
with default values being:
----------------------------
host='0.0.0.0' and port=5000
----------------------------
"""
from flask import Flask
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_db(exception: Exception):
    """
    Calls 'storage.close()'
    """
    storage.close()


if __name__ == "__main__":
    from os import getenv

    HOST = getenv('HBNB_API_HOST')
    PORT = getenv('HBNB_API_PORT')

    app.run(
        HOST if HOST else '0.0.0.0',
        PORT if PORT else 5000,
        threaded=True
    )
