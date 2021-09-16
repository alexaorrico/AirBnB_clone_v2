#!/usr/bin/python3
from flask import Flask
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)


if __name__ == '__main__':
    # runs the Flask application through port 5000 from local host
    app.run(host='0.0.0.0', port='5000', threaded=True)
