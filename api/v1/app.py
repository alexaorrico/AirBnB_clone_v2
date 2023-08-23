#!/usr/bin/python3
"""run script"""
from models import storage
from flask import Flask
from os import getenv


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_session(arg=None):
    "Close the session after each request"
    storage.close()


if __name__ == "__main__":
    """run the app"""
    from api.v1.views import app_views
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(getenv('HBNB_API_PORT', 5000))
    app.run(host=host, port=port, threaded=True)
