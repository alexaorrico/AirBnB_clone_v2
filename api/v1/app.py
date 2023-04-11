from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv


app = Flask(__name__)

app.register_blueprint(app_views)


@app.route('/andi')
def hello():
    return "Hello ennio"


@app.teardown_appcontext
def close_storage(exception):
    storage.close()


if __name__ == '__main__':
    host = '0.0.0.0'
    port = '5001'
    if getenv("HBNB_API_HOST"):
        host = getenv("HBNB_API_HOST")
    if getenv("HBNB_API_PORT"):
        port = getenv("HBNB_API_PORT")
    app.run(host=host, port=port, threaded=True, debug=True)
