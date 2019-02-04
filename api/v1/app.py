#!/usr/bin/python3
"""
Starts up a flask web app
"""
from flask import Flask
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_appcontext(response_or_exc):
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", threaded=True)
