#!/usr/bin/python3
""" flask API app """
from models import storage
from flask import Flask
from api.v1.views import app_views

app = Flask(__name__)

# app_views BluePrint defined in api.v1.views
app.register_blueprint(app_views)

@app.teardown_appcontext
def teardown_db(exception):
    """closes the storage on teardown"""
    storage.close()

if __name__ == "__main__":
    """ run the flask server """
    app.run(host='0.0.0.0', port=5000, threaded=True)