#!/usr/bin/python3
"""Flask App"""


from api.v1.views import app_views
from flask import Flask
from os import getenv
from models import storage


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(exception = None):
    """Closes storage on teardown"""
    storage.close()


if getenv("HBNB_API_HOST"):
    host = getenv("HBNB_API_HOST")
else:
    host = "0.0.0.0"

if getenv("HBNB_API_PORT"):
    port = int(getenv("HBNB_API_PORT"))
else:
    port = 5000


if __name__ == "__main__":
    """Main Function"""
    app.run(host=host, port=port)
