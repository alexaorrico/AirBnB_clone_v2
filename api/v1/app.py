#!/usr/bin/python3
import os
from flask import Flask, Blueprint, jsonify
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def tearDownDB():
    """removes sqlalchemy session"""
    storage.close()


# was unsure if we had environmental variables setup yet
if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', threaded=True)
    # app.run(os.getenv(HBNB_API_HOST),
    # os.getenv(HBNB_API_PORT), threaded=True)
