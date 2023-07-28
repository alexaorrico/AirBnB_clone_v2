from flask import Flask
from flask import sql_alchemy
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)


def downtear(self):
   """this method calls .close()"""
    storage.close()

if __name__ == "__main__":
    host = getenv('HBNB_API_HOST')
    port = getenv('HBNB_API_PORT')
    if not port:
        port = "5000"
    if not host:
        host = "0.0.0.0"
    app.run(host=host, port=port, threaded=True)
