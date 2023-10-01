from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from api.v1.views.index import api_v1_stats
import os

app = Flask(__name__)
app.register_blueprint(app_views, url_prefix='/api/v1')
app.register_blueprint(api_v1_stats)


@app.route('/nop')
def error_handler():
    response = {"error": "Not found"}
    return jsonify(response)


@app.teardown_appcontext
def teardown(exception):
    """
    calls the close() method
    """
    storage.close()


if __name__ == "__main__":
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', 5000))
    app.run(host=host, port=port, threaded=True)
