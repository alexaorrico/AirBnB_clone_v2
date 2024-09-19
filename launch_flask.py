import os
from api.v1.app import app

# Set environment variables
os.environ['HBNB_MYSQL_USER'] = 'hbnb_dev'
os.environ['HBNB_MYSQL_PWD'] = 'hbnb_dev_pwd'
os.environ['HBNB_MYSQL_HOST'] = 'localhost'
os.environ['HBNB_MYSQL_DB'] = 'hbnb_dev_db'
os.environ['HBNB_TYPE_STORAGE'] = 'db'
os.environ['HBNB_API_HOST'] = '0.0.0.0'
os.environ['HBNB_API_PORT'] = '5000'

# Retrieve the host and port from environment variables (with default values)
host = os.getenv('HBNB_API_HOST', '0.0.0.0')
port = int(os.getenv('HBNB_API_PORT', 5000))

# Launch the Flask app
if __name__ == "__main__":
    app.run(host=host, port=port, threaded=True)
