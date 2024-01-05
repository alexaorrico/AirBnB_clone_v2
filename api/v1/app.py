#!/usr/bin/python3
"""starts a flask application"""

from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views, url_prefix='/api/v1')

@app.teardown_appcontext
def teardown_db(exception):
    """calls storage.close"""
    storage.close()


if __name__ == '__main__':
    HOST = getenv('HBNB_API_HOST') if getenv('HBNB_API_HOST') else '0.0.0.0'
    PORT = getenv('HBNB_API_PORT') if getenv('HBNB_API_PORT') else 5000
    app.run(host=HOST, port=PORT, threaded=True)
