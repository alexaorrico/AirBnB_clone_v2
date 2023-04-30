#!/usr/bin/python3
"""
This is module 8-cities_by_state
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


@app.route('/states/')
@app.route('/states/<id_d>')
def cities_by_states(id_d="all"):
    states = storage.all("State")
    if id_d == "all":
        return render_template("9-states.html", state="all",
                               Query_name="States",
                               states=states.values())
    else:
        flag = False
        for k, v in states.items():
            if k == id_d:
                flag = True
                break
        if flag:
            result = v.cities
            return render_template("9-states.html", state="1",
                                   Query_name="State: {}".format(v.name),
                                   states=result)
        else:
            return render_template("9-states.html", state="",
                                   Query_name="Not found!",
                                   states=states)


@app.teardown_appcontext
def close_session(exception):
    """Remove the db session or save file"""
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
#    cities_by_states()
#    print("------------")
#    cities_by_states('421a55f4-7d82-47d9-b54c-a76916479556')
#    print("------------")
#    cities_by_states("hi")
