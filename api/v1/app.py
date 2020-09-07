#!/usr/bin/python3
"""[python script to set flask app]
"""
from flask import Flask, Blueprint
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(error):
    """[teardown method]

    Args:
        error ([type]): [description]
    """
    storage.close()

if __name__ == "__main__":
    app.run('0.0.0.0', 5000, threaded=True)
