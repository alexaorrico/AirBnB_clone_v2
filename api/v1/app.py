from api.v1.views import app_views
from flask import Flask, jsonify
from models import storage
import os


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_storage(exception=None):
    """Calls close storage at the end of each HTTP request"""
    storage.close()


@app.errorhandler(404)
def page_not_found(error):
    """returns 404 error"""
    return jsonify(error='Not found'), 404


if __name__ == '__main__':
    hbnb_host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    hbnb_port = int(os.getenv('HBNB_API_PORT', '5000'))
    app.run(host=hbnb_host, port=hbnb_port, threaded=True)
