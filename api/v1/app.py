#!/usr/bin/python3
""" API module """

from flask import Flask
from models import storage
from os import getenv
app = Flask(__name__)
from api.v1.views import app_views  # noqa: E402
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_appcontext(response_or_exc):
    """ close the session """
    storage.close()


if __name__ == "__main__":
    app.run(host=(getenv('HBNB_API_HOST') if getenv('HBNB_API_HOST')
                  else '0.0.0.0'),
            port=(getenv('HBNB_API_PORT') if getenv('HBNB_API_PORT')
                  else 5000),
            threaded=True)
