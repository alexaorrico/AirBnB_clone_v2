#!/usr/bin/python3
'''
Main file to run program
'''
from flask import Flask
from models import storage
from api.v1.views.index import app_views
from os import getenv


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(exception):
    '''Close connection'''
    storage.close()


if __name__ == '__main__':
    try:
        host = getenv('HBNB_API_HOST')
    except Exception as e:
        host = "0.0.0.0"

    try:
        port = getenv('HBNB_API_PORT')
    except Exception as e:
        port = 5000

    app.run(host=host, port=port, debug=True)
