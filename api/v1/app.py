#!/usr/bin/python3
"""for the following files"""
from flask import Flask
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(err):
    """Teardown the application"""
    storage.close()

@app.errorhandler(404)
def page_not_found(error):
    """loads a custom 404 page not found"""
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, threaded=True)
