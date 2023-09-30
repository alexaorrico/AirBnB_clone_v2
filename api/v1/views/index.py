from flask import Blueprint, jsonify
from flask import Flask
from api.v1.views import app_views
from models.engine import db_storage
# Define your routes within the blueprint
@app_views.route('/status')
def status():
    return jsonify({"status": "OK"})

app = Flask(__name__)

@app.route('/api/v1/stats')
def endpoint():
    stats = {}

    classes = [cls.__name__ for cls in db_storage.all().values()]

    for cls_name in set(classes):
        if cls_name != "BaseModel":
            stats[cls_name] = db_storage.count(cls_name)
    return jsonify(stats)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
