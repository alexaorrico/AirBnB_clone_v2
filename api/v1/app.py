#!/usr/bin/python3
"""
module to create Flask app that works with the API
"""
from models import storage
from flask import Flask
from api_views import app_views


app = Flask(__name__)
app.register_blueprint(app_views, url_previx="/api/vi")


@app.teardown_appcontext
def tear_down(self):
    "tears down"
    storage.close()


@app.errorhandler(404)
def not_found(error):
    "error handler for 404"
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == "__main__":
    host = os.getenv("HBNB_API_HOST", "0.0.0.0")
    port = int(os.getenv("HBNB_API_PORT", 5000))
    app.run(host=host, port=port, threaded=True)
