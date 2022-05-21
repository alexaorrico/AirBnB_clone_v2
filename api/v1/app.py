#!/usr/bin/python3
'''api'''

import os
from models import storage
from flask import Flask
from api.v1.views import app_views


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_storage(self):
    storage.close()


if __name__ == "__main__":
    host = os.environ.get('HBNB_API_HOST')
    if not host:
        host = '0.0.0.0'
    port = os.environ.get('HBNB_API_PORT')
    if not port:
        port = '5000'
    app.run(host=host, port=port)
