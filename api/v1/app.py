#!/usr/bin/ python3
# Barebones App
from flask import Flask
from models import storage
from api.v1.views import app_views
from flask
app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close(self):
    """
    Calls storage.close
    """
    storage.close()

if __name__ == '__main__':
    app.run(host=getenv("HBNB_API_HOST") or ("0.0.0.0"), port=(getenv("HBNB_API_PORT") or (5000)), (threaded=True))
