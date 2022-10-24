#!/usr/bin/python3
"""api"""
from flask import Flask
from models import storage
from api.v1.views import app_views

app = Flask(__name__)


app.register_blueprint(app_views)
@app.teardown_appcontext
def teardown(exception):
    """closes the storage on teardown"""
    storage.close()


if __name__ == '__main__':
    app.run(getenv('HBNB_API_HOST') or '0.0.0.0',
            getenv('HBNB_API_PORT') or 5000,
            threaded=True)
