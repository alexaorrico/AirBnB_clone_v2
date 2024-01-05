#!/usr/bin/python3

from flask import Flask

app = Flask('__name__')
from models import storage
from api.v1.views import app_views

app.register_blueprint(app_views)

@app.teardown_appcontext
def teardown_db(exception):
    """closes the storage on teardown"""
    storage.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', threaded=True)
