#!/usr/bin/python3
""" create a simple web application """
from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views, url_prefix='/api/v1')

host = getenv('HBNB_API_HOST', '0.0.0.0')
port = getenv('HBNB_API_PORT', '5000')


@app.teardown_appcontext
def teardown(self):
    """ teardown the app context, calls storage.close() """
    storage.close()


if __name__ == "__main__":
    app.run(host=host, port=port, threaded=True)