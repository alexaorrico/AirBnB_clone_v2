#!/usr/bin/python3

from api.v1.views import app_views
from flask import Flask
from models import storage

app = Flask(__name__)


app.register_blueprint(app_views)


@app.teardown_appcontext()
def teardown_appcontext():
    """
    This function is a Flask decorator that is used to register a function 
    to be called when the application context is torn down.
    """
    storage.close()


if __name__ == "__main__":
    HBNB_API_HOST = "0.0.0.0"
    HBNB_API_PORT = 5000
    app.run(host=HBNB_API_HOST, port=HBNB_API_PORT, threaded=True)
