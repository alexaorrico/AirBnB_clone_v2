#!/usr/bin/python3
""" creating default route """

from flask import Flask
from api.v1.views import app_views
from models import storage
import os

app = Flask(__name__)

app.register_blueprint(app_views, url_prefix='/api/v1')
app.url_map.strict_slashes = False


@app.teardown_appcontext
def teardown_storage(exception):
    """ closing storage """
    storage.close()


if __name__ == "__main__":
    """ just another flask app """
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', 5000))
    app.run(host=host, port=port, threaded=True)
