#!/usr/bin/python3
'''Initializing an app instance using Flask'''
from flask import Flask
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_storage(exc):
    '''Closing the database storage'''
    storage.close()


if __name__ == "__main__":
    host = os.environ.get("HBNB_API_HOST") or "0.0.0.0"
    port = os.environ.get("HBNB_API_PORT") or 5000
    app.run(host=host, port=port, threaded=True)
