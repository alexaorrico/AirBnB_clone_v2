import os
from flask import Flask, jsonify
from flask import make_response

from models import storage
from api.v1.views import app_views


app = Flask(__name__)
app.register_blueprint(app_views)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


@app.teardown_appcontext
def teardown_appcontext(response_or_exc):
    storage.close()

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    host = os.environ.get('HBNB_API_HOST') or "0.0.0.0"
    port = os.environ.get('HBNB_API_PORT') or '5000'
    app.run(host=host, port=port, threaded=True)
