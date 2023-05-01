#!/usr/bin/python3

<<<<<<< HEAD
"""configuring API"""

=======
>>>>>>> 59833b06c41e32f80b156b217b0a0f332b30db4f
from flask import Flask
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)
<<<<<<< HEAD
app.url_map.strict_slashes = False
=======

>>>>>>> 59833b06c41e32f80b156b217b0a0f332b30db4f
@app.teardown_appcontext
def teardown_appcontext(exception):
    storage.close()

<<<<<<< HEAD
if __name__ == '__main__':
    host = getenv("HBNB_API_HOST", "0.0.0.0")
    port = getenv("HBNB_API_PORT", "5000")
    app.run(host=host, port=port)
=======
if __name__ == "__main__":
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', 5000))
    app.run(host=host, port=port, threaded=True)
>>>>>>> 59833b06c41e32f80b156b217b0a0f332b30db4f
