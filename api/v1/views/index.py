#!/usr/bin/python3
""" index"""

from api.v1.views import app_views

app = Flask(_name__)
app.register_blueprint(app_views)

@app_views.route('/status', methods=['GET'])
def status():
    return jsonify ({'ststus: OK'})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
