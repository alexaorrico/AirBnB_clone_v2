#!/usr/bin/python3

from flask import Flask
from models import storage
from app.v1.views import app_views

app = Flask(__name__)
app.reg_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(self):
    """teardown"""
    storage.close()


if __name__ == '__main__':
    HBNB_API_HOST = getenv('HBNB_API_HOST')
    HBNB_API_PORT = getenv('HBNB_API_PORT')

    host = '0.0.0.0' if not HBNB_API_HOST else HBNB_API_HOST
    port = 5000 if not HBNB_API_PORT else HBNB_API_PORT
    app.run(host=host, port=port, threaded=True)
