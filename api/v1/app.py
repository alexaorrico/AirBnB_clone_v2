#!/usr/bin/python3
""" instance of Flask """
from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv as env


# create an instance of Flask
app = Flask(__name__)
# register blueprint
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(exception):
    """ close storage """
    storage.close()


def start_flask():
    """ start flask """
    app.run(host=env('HBNB_API_HOST'),
            port=env('HBNB_API_PORT'),
            threaded=True)

if __name__ == "__main__":
    start_flask()
