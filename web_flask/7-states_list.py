#!/usr/bin/python3
"""hello flask"""
from flask import Flask, render_template
from models import storage


app = Flask(__name__)


@app.route("/states_list")
def get_states_list():
    return render_template("7-states_list.html", storage=storage.all('State'))


@app.teardown_appcontext
def close_storage(exception):
    storage.close()


if __name__ == '__main__':
    app.url_map.strict_slashes = False
    app.run(host='0.0.0.0', port=5000)
