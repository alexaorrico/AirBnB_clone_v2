#!/usr/bin/python3
from models import storage
from api.v1.views import app_views
from flask import Flask, Blueprint, jsonify

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown():
    ''' Closes current storage session '''
    storage.close()


if __name__ == "__main__":
    app.run(HBNB_API_HOST, HBNB_API_PORT, threaded=True)
