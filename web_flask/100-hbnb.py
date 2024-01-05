#!/usr/bin/python3
"""a module that starts a flask web application on 0.0.0.0 port 5000"""
from flask import Flask, render_template, Markup
from markupsafe import escape
import os
import subprocess

current_directory = os.getenv("PWD")
storage = None
storage_type = os.getenv("HBNB_TYPE_STORAGE")
app = Flask(__name__)
if current_directory:
    import sys
    old_directory = current_directory
    current_directory = current_directory.split('/')
    current_directory = current_directory[:-1]
    current_directory = '/'.join(current_directory)
    flask_directory = (f"{old_directory}/web_flask")
    sys.path.append(current_directory)
    sys.path.append(flask_directory)
    from models import storage
    from models.state import State
    from models.city import City
    from models.amenity import Amenity
    from models.place import Place

if storage:
    @app.route('/', strict_slashes=False)
    def index():
        """a route handler for the root route"""
        return "Hello HBNB!"

    @app.route('/c/<text>', strict_slashes=False)
    def c_route(text):
        """a route handler for the /c/[slug]"""
        return f"C {escape(text.replace('_', ' '))}"

    @app.route('/python/<text>', strict_slashes=False)
    @app.route('/python/', defaults={'text': None}, strict_slashes=False)
    def py_route(text):
        """a route handler for the /python/[slug]"""
        if text:
            return f"Python {escape(text.replace('_', ' '))}"
        return "Python is cool"

    @app.route('/number/<int:n>', strict_slashes=False)
    def num_route(n):
        """a route handler for the /number/[slug]"""
        return f"{escape(n)} is a number"

    @app.route('/number_template/<int:n>', strict_slashes=False)
    def num_template_route(n):
        """a route handler for the /number_template/[slug]"""
        return render_template('5-number.html', n=n)

    @app.route('/number_odd_or_even/<int:n>', strict_slashes=False)
    def num_odd_even(n):
        """a route handler for the /number_odd_or_even/[slug]"""
        return render_template('6-number_odd_or_even.html', n=n)

    @app.route('/states_list')
    def handle_states_list():
        """this is the route handler for the /states_list endpoint"""
        all_states = storage.all('State')
        all_states = sorted(all_states.items(), key=lambda x: x[1].name)
        return render_template('7-states_list.html', states=all_states)

    @app.route('/cities_by_states')
    def handle_state_cities_list():
        """this is the route handler for the /states_list endpoint"""
        all_states = storage.all('State')
        for value in all_states.values():
            # value.cities = sorted(value.cities, key=lambda x: x[1].name)
            if value.cities:
                value.cities = sorted(value.cities, key=lambda x: x.name)
        all_states = sorted(all_states.items(), key=lambda x: x[1].name)

        return render_template('8-cities_by_states.html', states=all_states)

    @app.route("/states", strict_slashes=False)
    def states():
        """route handler for /states endpoint"""
        states = storage.all('State')
        states = dict(sorted(states.items(), key=lambda item: item[1].name))
        return render_template('9-states.html',
                               not_found=False, data=states, id=None)

    @app.route("/states/<id>", strict_slashes=False)
    def states_id(id):
        """the route handler for the endpoint /statses/[slug]"""
        state = storage.search(State, id=id)
        if state is None:
            return render_template('9-states.html',
                                   not_found=True, data=states)
        c = storage.all('City')
        cities = {}
        for key, city in c.items():
            if state.id == city.state_id:
                cities[key] = city
        cities = sorted(cities.items(), key=lambda item: item[1].name)
        return render_template('9-states.html', name=state.name,
                               not_found=False, cities=cities, id=1)

    @app.route("/hbnb_filters", strict_slashes=False)
    def hbnb_filter():
        """route handler for /hbnb_filters endpoint"""
        res_data = {}
        states = storage.all('State')
        cities = storage.all('City')
        amenities = storage.all('Amenity')
        states = sorted(states.items(), key=lambda item: item[1].name)
        cities = sorted(cities.items(), key=lambda item: item[1].name)
        amenities = sorted(amenities.items(), key=lambda item: item[1].name)
        res_data["cities"] = cities
        res_data["states"] = states
        res_data["amenities"] = amenities
        # for value in res_data["states"]:
        #     print(f"states: {value}")
        return render_template('10-hbnb_filters.html', data=res_data)

    @app.route("/hbnb", strict_slashes=False)
    def hbnb_route():
        """route handler for /hbnb endpoint"""
        res_data = {}
        states = storage.all('State')
        cities = storage.all('City')
        amenities = storage.all('Amenity')
        places = storage.all('Place')
        states = sorted(states.items(), key=lambda item: item[1].name)
        cities = sorted(cities.items(), key=lambda item: item[1].name)
        amenities = sorted(amenities.items(), key=lambda item: item[1].name)
        places = sorted(places.items(), key=lambda item: item[1].name)
        res_data["cities"] = cities
        res_data["states"] = states
        res_data["amenities"] = amenities
        res_data["places"] = places
        for value in res_data["places"]:
            user = [x for x in storage.all('User').values()
                    if x.id == value[1].user_id]
            if user:
                value[1].owner = f"{user[0].first_name} {user[0].last_name}"
            else:
                value[1].owner = ""
            value[1].description = Markup(value[1].description)
        return render_template('100-hbnb.html', data=res_data)

    def teardown_requests(exception=None):
        """this is the teardown function to be executed in the"""
        storage.close()

    app.teardown_appcontext(teardown_requests)

    if __name__ == "__main__":
        app.run(host='0.0.0.0', port=5000, debug=True)
