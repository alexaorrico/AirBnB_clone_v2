import os
from flask import Flask
from models.engine import storage
from views import app_views

app = Flask(__name__)

@app.teardown_appcontext
def teardown():
    storage.close()


if __name__ == '__main__':
    host = os.environ.get('HBNB_API_HOST') or "0.0.0.0"
    port = os.environ.get('HBNB_API_PORT') or '5000'
    app.run(host=host, port=port, threaded=True)
