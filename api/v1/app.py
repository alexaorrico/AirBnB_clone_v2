#!usr/bin/python3
'''
    API for AirBnb clone
'''

from os import getenv
from flask import Flask, Blueprint
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_close(msg=None):
    storage.close()

if __name__ == "__main__":
    port = getenv('HBNB_API_PORT', '5000')
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    app.run(host, int(port), threaded=True)
