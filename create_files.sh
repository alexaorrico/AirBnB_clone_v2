#!/bin/bash

# Create the api directory
mkdir api
touch api/__init__.py

# Create the api/v1 directory
mkdir api/v1
touch api/v1/__init__.py

# Create the api/v1/app.py file
echo -e "#!/usr/bin/python3\n\nfrom flask import Flask\nfrom models import storage\nfrom api.v1.views import app_views\nimport os\n\napp = Flask(__name__)\n\napp.register_blueprint(app_views, url_prefix=\"/api/v1\")\n\n@app.teardown_appcontext\ndef teardown_appcontext(exception):\n    storage.close()\n\nif __name__ == \"__main__\":\n    host = os.getenv(\"HBNB_API_HOST\") or \"0.0.0.0\"\n    port = int(os.getenv(\"HBNB_API_PORT\") or 5000)\n    app.run(host=host, port=port, threaded=True)" > api/v1/app.py

# Create the api/v1/views directory
mkdir api/v1/views
touch api/v1/views/__init__.py

# Create the api/v1/views/index.py file
echo -e "from flask import jsonify\nfrom api.v1.views import app_views\n\n@app_views.route('/status', methods=['GET'], strict_slashes=False)\ndef status():\n    return jsonify({\"status\": \"OK\"})" > api/v1/views/index.py

