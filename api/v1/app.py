#!/usr/bin/python3
"""Flask App"""

from api.v1.views import app_views
from flask import Flask
from os import getenv
from models import storage


app = Flask(__name__)
app.register_blueprint(app_views)
app.url_map.strict_slashes = False



@app.teardown_appcontext
def teardown_db(exception):
    """Closes storage on teardown"""
    storage.close()


if __name__ == "__main__":
    """Main Function"""
    port = 5000
    host = '0.0.0.0'
    app.run(host=host, port=port)