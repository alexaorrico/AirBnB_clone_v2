#!/usr/bin/python3
"""Defines unittests for api/."""
import os
import unittest
from models import storage
from models.base_model import Base
from models.city import City
from models.state import State
from api.v1.app import app


class HolbertonBnBTestCase(unittest.TestCase):
    """Unittests for testing the HolbertonBnB API."""

    @classmethod
    def setUpClass(cls):
        """Initialize the test client."""
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        cls.state = State(name="California")
        cls.state.save()
        cls.city = City(name="San Francisco", state_id=cls.state.id)
        cls.city.save()
        cls.__app = app.test_client()

    @classmethod
    def tearDownClass(cls):
        """Drop DBStorage metadata before finishing."""
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass
        if (os.getenv("HBNB_TYPE_STORAGE") == "db" and
                os.getenv("HBNB_ENV") == "test"):
            Base.metadata.drop_all(storage._DBStorage__engine)

    def test_404(self):
        """Test custom 404 error handler."""
        with self.__app as a:
            resp = a.get("/api/v1/error", follow_redirects=True)
            self.assertEqual(resp.status_code, 404)
            self.assertDictEqual(resp.get_json(), {"error": "Not found"})

    def test_server_status(self):
        """Test /status route."""
        with self.__app as a:
            resp = a.get("/api/v1/status", follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertDictEqual(resp.get_json(), {"status": "OK"})

    def test_stats(self):
        """Test /stats route"""
        with self.__app as a:
            resp = a.get("/api/v1/stats", follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            with open("file.json", encoding="utf-8") as f:
                sample = {
                    "amenities": storage.count("Amenity"),
                    "cities": storage.count("City"),
                    "places": storage.count("Place"),
                    "reviews": storage.count("Review"),
                    "states": storage.count("State"),
                    "users": storage.count("User")
                }
            self.assertEqual(sample, resp.get_json())

    def test_states_get(self):
        """Test GET method on /states route."""
        with self.__app as a:
            resp = a.get("/api/v1/states", follow_redirects=True)
            states = [s.to_dict() for s in storage.all("State").values()]
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.get_json(), states)

    def test_states_get_id(self):
        """Test GET method with specific id on /states route."""
        with self.__app as a:
            resp = a.get("/api/v1/states/{}".format(self.state.id),
                         follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertDictEqual(self.state.to_dict(), resp.get_json())

    def test_states_post(self):
        """Test POST method on /states route."""
        with self.__app as a:
            data = {"name": "Washington"}
            count = storage.count()
            resp = a.post("/api/v1/states", json=data, follow_redirects=True)
            msg = resp.get_json()
            self.assertEqual(resp.status_code, 201)
            self.assertEqual(msg.get("__class__"), "State")
            self.assertEqual(msg.get("name"), "Washington")
            self.assertGreater(storage.count(), count)

    def test_states_bad_post(self):
        """Test POST method with bad JSON format on /states route."""
        with self.__app as a:
            resp = a.post("/api/v1/states", data="bad", follow_redirects=True)
            self.assertEqual(resp.status_code, 400)
            self.assertIn(b"Not a JSON", resp.data)

    def test_states_post_missing_name(self):
        """Test POST method with missing name in JSON on /states route."""
        with self.__app as a:
            resp = a.post("/api/v1/states", json={"missing": "name"},
                          follow_redirects=True)
            self.assertEqual(resp.status_code, 400)
            self.assertIn(b"Missing name", resp.data)

    def test_states_delete(self):
        """Test DELETE method on /states route."""
        state = State(name="Virginia")
        state.save()
        with self.__app as a:
            resp = a.delete("/api/v1/states/{}".format(state.id),
                            follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertDictEqual(resp.get_json(), {})
            self.assertNotIn(state, list(storage.all("State").values()))

    def test_states_bad_delete(self):
        """Test DELETE method with nonexistant object on /states route."""
        with self.__app as a:
            resp = a.delete("/api/v1/states/bad", follow_redirects=True)
            self.assertEqual(resp.status_code, 404)

    def test_states_put(self):
        """Test PUT method on /states route."""
        with self.__app as a:
            data = {"name": "Golden State"}
            resp = a.put("/api/v1/states/{}".format(self.state.id),
                         json=data, follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.get_json().get("name"), "Golden State")
            self.assertEqual(storage.get("State", self.state.id).name,
                             "Golden State")

    def test_states_bad_put(self):
        """Test PUT method with invalid state on /states route."""
        with self.__app as a:
            resp = a.put("/api/v1/states/bad", follow_redirects=True)
            self.assertEqual(resp.status_code, 404)

    def test_states_bad_put_data(self):
        """Test PUT method with invalid JSON data on /states route."""
        with self.__app as a:
            resp = a.put("/api/v1/states/{}".format(self.state.id),
                         data="bad", follow_redirects=True)
            self.assertEqual(resp.status_code, 400)
            self.assertIn(b"Not a JSON", resp.data)

    def test_cities_get(self):
        """Test GET method on /cities route."""
        with self.__app as a:
            resp = a.get("/api/v1/states/{}/cities".format(self.state.id),
                         follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            cities = [city.to_dict() for city in self.state.cities]
            self.assertEqual(resp.get_json(), cities)

    def test_cities_get_id(self):
        """Test GET method with specific id on /cities route."""
        with self.__app as a:
            resp = a.get("/api/v1/cities/{}".format(self.city.id),
                         follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertDictEqual(self.city.to_dict(), resp.get_json())

    def test_cities_post(self):
        """Test POST method on /cities route."""
        with self.__app as a:
            data = {"name": "Eureka"}
            count = storage.count()
            resp = a.post("/api/v1/states/{}/cities".format(self.state.id),
                          json=data, follow_redirects=True)
            msg = resp.get_json()
            self.assertEqual(resp.status_code, 201)
            self.assertEqual(msg.get("__class__"), "City")
            self.assertEqual(msg.get("name"), "Eureka")
            self.assertGreater(storage.count(), count)

    def test_cities_bad_post(self):
        """Test POST method with bad JSON format on /cities route."""
        with self.__app as a:
            resp = a.post("/api/v1/states/{}/cities".format(
                self.state.id), data="bad", follow_redirects=True)
            self.assertEqual(resp.status_code, 400)
            self.assertIn(b"Not a JSON", resp.data)

    def test_cities_post_missing_name(self):
        """Test POST method with missing name in JSON on /cities route."""
        with self.__app as a:
            resp = a.post("/api/v1/states/{}/cities".format(self.state.id),
                          json={"missing": "name"}, follow_redirects=True)
            self.assertEqual(resp.status_code, 400)
            self.assertIn(b"Missing name", resp.data)

    def test_cities_delete(self):
        """Test DELETE method on /states route."""
        city = City(name="Los Angeles")
        city.save()
        with self.__app as a:
            resp = a.delete("/api/v1/cities/{}".format(city.id),
                            follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertDictEqual(resp.get_json(), {})
            self.assertNotIn(city, list(storage.all("City").values()))

    def test_cities_bad_delete(self):
        """Test DELETE method with nonexistant object on /cities route."""
        with self.__app as a:
            resp = a.delete("/api/v1/cities/bad", follow_redirects=True)
            self.assertEqual(resp.status_code, 404)

    def test_cities_put(self):
        """Test PUT method on /cities route."""
        city = City(name="San Diego")
        city.save()
        with self.__app as a:
            data = {"name": "Padres"}
            resp = a.put("/api/v1/cities/{}".format(city.id),
                         json=data, follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.get_json().get("name"), "Padres")
            self.assertEqual(storage.get("City", city.id).name,
                             "Padres")

    def test_cities_bad_put(self):
        """Test PUT method with invalid city on /cities route."""
        with self.__app as a:
            resp = a.put("/api/v1/cities/bad", follow_redirects=True)
            self.assertEqual(resp.status_code, 404)

    def test_cities_bad_put_data(self):
        """Test PUT method with invalid JSON data on /cities route."""
        with self.__app as a:
            resp = a.put("/api/v1/cities/{}".format(self.city.id),
                         data="bad", follow_redirects=True)
            self.assertEqual(resp.status_code, 400)
            self.assertIn(b"Not a JSON", resp.data)
