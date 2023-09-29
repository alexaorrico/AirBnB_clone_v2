#!/usr/bin/python3
""" """


from flask import Flask
from models import storage
from api.v1.views import app_views
from os import environ
app = Flask(__name__)


app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    storage.close()


if __name__ == '__main__':
    hst = environ.get("HBNB_API_HOST") if environ.get("HBNB_API_HOST") else "0.0.0.0"
    prt = environ.get("HBNB_API_PORT") if environ.get("HBNB_API_PORT") else 5000
    app.run(host=hst, port=prt, threaded=True)
