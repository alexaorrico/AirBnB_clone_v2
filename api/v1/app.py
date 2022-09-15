#!/usr/bin/python3
from os import getenv
from models import storage
from api.v1.views import app_views
from flask import Flask
from werkzeug.exceptions import HTTPException
import json


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(exception):
    """closes the storage on teardown"""
    storage.close()


@app.errorhandler(HTTPException)
def handle_exception(e):
    return json.dumps({'error': 'Not found'}, indent=4)


if __name__ == '__main__':
    db_host = getenv('HBNB_API_HOST', default='0.0.0.0')
    db_port = getenv('HBNB_API_PORT', default='5000')
    app.run(host=db_host, port=db_port, threaded=True)
