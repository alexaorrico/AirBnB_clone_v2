#!/usr/bin/python3
"""
starts a Flask web application
"""
from api.v1.views import app_views
from models import storage
from flask import Flask
app = Flask(__name__)

app.register_blueprint(app_views)

@app.teardown_appcontext
def teardown_db(exception):
    """closes the storage on teardown"""
    storage.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', threaded=True)