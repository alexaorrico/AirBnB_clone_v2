from flask import Flask
from flask import Blueprint
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)

@app.teardown_appcontext
def shut(exec):
    storage.close()

if __name__ == "__main__":
    app.run(getenv('HBNB_API_HOST'), getenv('HBNB_API_PORT'), threaded=True)
