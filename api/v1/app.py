#!/usr/bin/python3
""" flusk app """

from api.v1.views import app_views
from flask import Flask
from models import storage
from os import getenv
from flask import jsonify



app = Flask(__name__)

app.register_blueprint(app_views)


@app.teardown_appcontext
def tear_down(e):
    """ teardown for app """
    storage.close()


@app.errorhandler(404)
def no_page(e):
    """ displays a 404 json mesage """
    return jsonify({'errorCode' : 404,"error": "Not found"}), 404


if __name__ == "__main__":
    """ ran the app """
    app.run(host=getenv('HBNB_API_HOST'),
            port=getenv('HBNB_API_PORT'), threaded=True)
