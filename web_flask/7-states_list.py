#!/usr/bin/python3
"""
This is module 7-states_list
In this module we combine flask with sqlAlchemy for the first time
Run this script from AirBnB_v2 directory for imports
"""
from models import storage
from models.base_model import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from os import getenv
from models.user import User
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from flask import Flask
from flask import render_template
app = Flask(__name__)


@app.route('/states_list/')
def list_states():
    """list all states in a db"""
    states = storage.all("State").values()
    return render_template("7-states_list.html",
                           Query_name="States", states=states)


@app.teardown_appcontext
def close_session(exception):
    """remove the session to see what happened"""
    storage.close()


if __name__ == "__main__":
        app.run(host="0.0.0.0", port="5300")
