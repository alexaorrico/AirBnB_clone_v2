#!/usr/bin/python3
""" Flask application """

from api.v1.views import app_views
from flask import Flask
from models import storage

app = Flask(__name__)

app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    '''what should happen when the app is getting teared down'''
    if storage is not None:
        storage.close()


if __name__ == '__main__':
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = os.getenv('HBNB_API_PORT', '5000')
    app.run(host=host, port=port, threaded=True)
