#!/usr/bin/python3
""""""
from flask import jsonify
from api.v1.views import app_views
app_views.url_map.strict_slashes = False


@app_views.route('/status')
def status():
    return jsonify({'status': 'OK'})


if __name__ == "__main__":
    app_views.run(host='0.0.0.0', port=5000, threaded=True)
