from flask import Flask 
from flask import Blueprint
from models import storage
from api.v1.views import app_views


app = Flask(__name__)
app.register_blueprint(app_views)
# app_views = Blueprint('app_views', __name__)

@app.teardown_appcontext()
def teardown_()
    storage.close()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000,threaded=True)

