"""Flask file"""

from api.v1.views import app_views
from flask import Flask
from models import storage

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def clean_up(exception=None):
    """elminate current session"""
    storage.close()


if __name__ == "__main__":
