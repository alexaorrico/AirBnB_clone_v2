from flask import Flask
from flask_cors import CORS
from models import storage
from api.v1.views import app_views
from os import getenv


app = Flask(__name__)
CORS(app, origins="0.0.0.0")
app.register_blueprint(app-views)

@app.teardown_appcontext
def teardown(self):
    """function that close queries"""
    storage.close()

if __name__ == "__main__":
    app.run(host=getenv("HBNB_API_HOST", "0.0.0.0"),
        port=int(getenv("HBNB_API_PORT", "5000")), threaded=True)
