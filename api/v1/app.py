import models
from api.v1.views import app_views
from flask import Flask, make_response, jsonify
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)


@app.errorhandler(404)
def notfound(error):
    """Handles 404 error"""
    jsonFile = jsonify({"error": "Not found"})
    return make_response(jsonFile, 404)


@app.teardown_appcontext
def teardown_app(self):
    models.storage.close()


if __name__ == "__main__":
    host = getenv("HBNB_API_HOST", "0.0.0.0")
    port = int(getenv("HBNB_API_PORT", 5000))
    app.run(host=host, port=port, threading=True)
