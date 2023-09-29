#!/usr/bin/python3
from flask import Flask, blueprint
from models import storage
from api.v1.views import app_views

HBNB_API_HOST = '0.0.0.0'
HBNB_API_PORT = 5000
app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext(app)
def teardown_app(app):
    return storage.close(app)


if __name__ == '__main__':
    app.run(host='HBNB_API_HOST', port=HBNB_API_PORT, threaded=True)
