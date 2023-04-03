#!/usr/bin/python3
'''task 4'''
from flask import Flask, Blueprint
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)

app.register_blueprint(app_views)


@app.tearddown_appcontext
=======
@app.teardown_appcontext

def tearitup():
    """turrupboii"""
    storage.close()


if __name__ == '__main__':
=======
def start_flask():
    """ start flask """

    app.run(host=getenv('HBNB_API_HOST'),
            port=getenv('HBNB_API_PORT'),
            threaded=True)


if __name__ == "__main__":
    start_flask()
