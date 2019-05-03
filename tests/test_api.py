#!/usr/bin/python3
"""Defines unittests for api/."""
import os
import unittest
from models import storage
from models.base_model import Base
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from api.v1.app import app


class HolbertonBnBTestCase(unittest.TestCase):
    """Unittests for testing the HolbertonBnB API."""

    @classmethod
    def setUpClass(cls):
        """Initialize the test client with a sample database."""
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        cls.state = State(name="California")
        cls.state.save()
        cls.city = City(name="San Francisco", state_id=cls.state.id)
        cls.city.save()
        cls.amenity = Amenity(name="Internet")
        cls.amenity.save()
        cls.user = User(email="holberton@holberton.com", password="pwd")
        cls.user.save()
        cls.place = Place(name="School",
                          city_id=cls.city.id, user_id=cls.user.id)
        cls.amenity_2 = Amenity(name="bed")
        cls.amenity_2.save()
        if os.getenv("HBNB_TYPE_STORAGE") == "db":
            cls.place.amenities.append(cls.amenity_2)
        else:
            cls.place.amenity_ids.append(cls.amenity_2.id)

        cls.place.save()
        cls.review = Review(text="Stellar",
                            place_id=cls.place.id, user_id=cls.user.id)
        cls.review.save()
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
        if os.getenv("HBNB_MYSQL_DB") == "hbnb_test_db":
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
            self.assertEqual(self.state.id, resp.get_json().get("id"))

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
            self.assertEqual(storage.count(), count + 1)

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
            data = {
                "name": "Golden State",
                "id": "avoid",
                "created_at": "avoid",
                "updated_at": "avoid"
            }
            resp = a.put("/api/v1/states/{}".format(self.state.id),
                         json=data, follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.get_json().get("name"), "Golden State")
            state = storage.get("State", self.state.id)
            self.assertEqual(state.name, "Golden State")
            self.assertNotEqual(state.id, "avoid")
            self.assertNotEqual(state.created_at, "avoid")
            self.assertNotEqual(state.updated_at, "avoid")

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
            self.assertIn(storage.get(
                "City", self.city.id).to_dict(), resp.get_json())

    def test_cities_get_id(self):
        """Test GET method with specific id on /cities route."""
        with self.__app as a:
            resp = a.get("/api/v1/cities/{}".format(self.city.id),
                         follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(self.city.id, resp.get_json().get("id"))

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

    def test_cities_post_bad_state(self):
        """Test POST method with bad state_id in JSON on /cities route."""
        with self.__app as a:
            resp = a.post("/api/v1/states/bad/cities", json={"tmp": "tmp"},
                          follow_redirects=True)
            self.assertEqual(resp.status_code, 404)

    def test_cities_delete(self):
        """Test DELETE method on /states route."""
        city = City(name="Los Angeles", state_id=self.state.id)
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
        with self.__app as a:
            data = {
                "name": "Padres",
                "id": "avoid",
                "state_id": "avoid",
                "created_at": "avoid",
                "updated_at": "avoid",
            }
            resp = a.put("/api/v1/cities/{}".format(self.city.id),
                         json=data, follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.get_json().get("name"), "Padres")
            city = storage.get("City", self.city.id)
            self.assertEqual(city.name, "Padres")
            self.assertNotEqual(city.id, "avoid")
            self.assertNotEqual(city.state_id, "avoid")
            self.assertNotEqual(city.created_at, "avoid")
            self.assertNotEqual(city.updated_at, "avoid")

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

    def test_amenities_get(self):
        """Test GET method on /amenities route."""
        with self.__app as a:
            resp = a.get("/api/v1/amenities".format(self.amenity.id),
                         follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            amenities = [a.to_dict() for a in storage.all("Amenity").values()]
            self.assertEqual(resp.get_json(), amenities)

    def test_amenities_get_id(self):
        """Test GET method with specific id on /amenities route."""
        with self.__app as a:
            resp = a.get("/api/v1/amenities/{}".format(self.amenity.id),
                         follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(self.amenity.id, resp.get_json().get("id"))

    def test_amenities_post(self):
        """Test POST method on /amenities route."""
        with self.__app as a:
            data = {"name": "Eureka"}
            count = storage.count("Amenity")
            resp = a.post("/api/v1/amenities".format(self.amenity.id),
                          json=data, follow_redirects=True)
            msg = resp.get_json()
            self.assertEqual(resp.status_code, 201)
            self.assertEqual(msg.get("__class__"), "Amenity")
            self.assertEqual(msg.get("name"), "Eureka")
            self.assertGreater(storage.count("Amenity"), count)

    def test_amenities_bad_post(self):
        """Test POST method with bad JSON format on /amenities route."""
        with self.__app as a:
            resp = a.post("/api/v1/amenities".format(
                self.amenity.id), data="bad", follow_redirects=True)
            self.assertEqual(resp.status_code, 400)
            self.assertIn(b"Not a JSON", resp.data)

    def test_amenities_post_missing_name(self):
        """Test POST method with missing name in JSON on /amenities route."""
        with self.__app as a:
            resp = a.post("/api/v1/amenities".format(self.amenity.id),
                          json={"missing": "name"}, follow_redirects=True)
            self.assertEqual(resp.status_code, 400)
            self.assertIn(b"Missing name", resp.data)

    def test_amenities_delete(self):
        """Test DELETE method on /amenities route."""
        amenity = Amenity(name="Water")
        amenity.save()
        with self.__app as a:
            resp = a.delete("/api/v1/amenities/{}".format(amenity.id),
                            follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertDictEqual(resp.get_json(), {})
            self.assertNotIn(amenity, list(storage.all("Amenity").values()))

    def test_amenities_bad_delete(self):
        """Test DELETE method with nonexistant object on /amenities route."""
        with self.__app as a:
            resp = a.delete("/api/v1/amenities/bad", follow_redirects=True)
            self.assertEqual(resp.status_code, 404)

    def test_amenities_put(self):
        """Test PUT method on /amenities route."""
        with self.__app as a:
            data = {
                "name": "Electricity",
                "id": "avoid",
                "created_at": "avoid",
                "updated_at": "avoid",
            }
            resp = a.put("/api/v1/amenities/{}".format(self.amenity.id),
                         json=data, follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.get_json().get("name"), "Electricity")
            amenity = storage.get("Amenity", self.amenity.id)
            self.assertEqual(amenity.name, "Electricity")
            self.assertNotEqual(amenity.id, "avoid")
            self.assertNotEqual(amenity.created_at, "avoid")
            self.assertNotEqual(amenity.updated_at, "avoid")

    def test_amenities_bad_put(self):
        """Test PUT method with invalid amenity on /amenities route."""
        with self.__app as a:
            resp = a.put("/api/v1/amenities/bad", follow_redirects=True)
            self.assertEqual(resp.status_code, 404)

    def test_amenities_bad_put_data(self):
        """Test PUT method with invalid JSON data on /amenities route."""
        with self.__app as a:
            resp = a.put("/api/v1/amenities/{}".format(self.amenity.id),
                         data="bad", follow_redirects=True)
            self.assertEqual(resp.status_code, 400)
            self.assertIn(b"Not a JSON", resp.data)

    def test_users_get(self):
        """Test GET method on /users route."""
        with self.__app as a:
            resp = a.get("/api/v1/users".format(self.user.id),
                         follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            users = [u.to_dict() for u in storage.all("User").values()]
            self.assertEqual(resp.get_json(), users)

    def test_users_get_id(self):
        """Test GET method with specific id on /users route."""
        with self.__app as a:
            resp = a.get("/api/v1/users/{}".format(self.user.id),
                         follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(self.user.id, resp.get_json().get("id"))

    def test_users_post(self):
        """Test POST method on /users route."""
        with self.__app as a:
            data = {"email": "h@h.com", "password": "dwp"}
            count = storage.count("User")
            resp = a.post("/api/v1/users".format(self.user.id),
                          json=data, follow_redirects=True)
            msg = resp.get_json()
            self.assertEqual(resp.status_code, 201)
            self.assertEqual(msg.get("__class__"), "User")
            self.assertEqual(msg.get("email"), "h@h.com")
            self.assertIsNone(msg.get("password"))
            self.assertGreater(storage.count("User"), count)

    def test_users_bad_post(self):
        """Test POST method with bad JSON format on /users route."""
        with self.__app as a:
            resp = a.post("/api/v1/users".format(
                self.user.id), data="bad", follow_redirects=True)
            self.assertEqual(resp.status_code, 400)
            self.assertIn(b"Not a JSON", resp.data)

    def test_users_post_missing_email(self):
        """Test POST method with missing name in JSON on /users route."""
        with self.__app as a:
            resp = a.post("/api/v1/users".format(self.user.id),
                          json={"missing": "email"}, follow_redirects=True)
            self.assertEqual(resp.status_code, 400)
            self.assertIn(b"Missing email", resp.data)

    def test_users_post_missing_password(self):
        """Test POST method with missing name in JSON on /users route."""
        with self.__app as a:
            resp = a.post("/api/v1/users".format(self.user.id),
                          json={"email": "here", "missing": "password"},
                          follow_redirects=True)
            self.assertEqual(resp.status_code, 400)
            self.assertIn(b"Missing password", resp.data)

    def test_users_delete(self):
        """Test DELETE method on /users route."""
        user = User(email="test_email", password="test_password")
        user.save()
        with self.__app as a:
            resp = a.delete("/api/v1/users/{}".format(user.id),
                            follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertDictEqual(resp.get_json(), {})
            self.assertNotIn(user, list(storage.all("User").values()))

    def test_users_bad_delete(self):
        """Test DELETE method with nonexistant object on /users route."""
        with self.__app as a:
            resp = a.delete("/api/v1/users/bad", follow_redirects=True)
            self.assertEqual(resp.status_code, 404)

    def test_users_put(self):
        """Test PUT method on /users route."""
        with self.__app as a:
            data = {
                "password": "new",
                "id": "avoid",
                "email": "avoid",
                "created_at": "avoid",
                "updated_at": "avoid",
            }
            original = self.user.id
            resp = a.put("/api/v1/users/{}".format(self.user.id),
                         json=data, follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertNotEqual(resp.get_json().get("password"), original)
            user = storage.get("User", self.user.id)
            self.assertNotEqual(user.password, original)
            self.assertNotEqual(user.id, "avoid")
            self.assertNotEqual(user.email, "avoid")
            self.assertNotEqual(user.created_at, "avoid")
            self.assertNotEqual(user.updated_at, "avoid")

    def test_users_bad_put(self):
        """Test PUT method with invalid user on /users route."""
        with self.__app as a:
            resp = a.put("/api/v1/users/bad", follow_redirects=True)
            self.assertEqual(resp.status_code, 404)

    def test_users_bad_put_data(self):
        """Test PUT method with invalid JSON data on /users route."""
        with self.__app as a:
            resp = a.put("/api/v1/users/{}".format(self.user.id),
                         data="bad", follow_redirects=True)
            self.assertEqual(resp.status_code, 400)
            self.assertIn(b"Not a JSON", resp.data)

    @unittest.skipIf(os.getenv("HBNB_TYPE_STORAGE") != "db",
                     "Testing DBStorage")
    def test_places_get(self):
        """Test GET method on /places route."""
        with self.__app as a:
            resp = a.get("/api/v1/cities/{}/places".format(self.city.id),
                         follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn(storage.get("Place", self.place.id).to_dict(),
                          resp.get_json())

    def test_places_get_id(self):
        """Test GET method with specific id on /places route."""
        with self.__app as a:
            resp = a.get("/api/v1/places/{}".format(self.place.id),
                         follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(self.place.id, resp.get_json().get("id"))

    def test_places_post(self):
        """Test POST method on /places route."""
        with self.__app as a:
            data = {
                "name": "Bathroom",
                "user_id": self.user.id,
            }
            count = storage.count()
            resp = a.post("/api/v1/cities/{}/places".format(self.city.id),
                          json=data, follow_redirects=True)
            msg = resp.get_json()
            self.assertEqual(resp.status_code, 201)
            self.assertEqual(msg.get("__class__"), "Place")
            self.assertEqual(msg.get("name"), "Bathroom")
            self.assertGreater(storage.count(), count)

    def test_places_bad_post(self):
        """Test POST method with bad JSON format on /places route."""
        with self.__app as a:
            resp = a.post("/api/v1/cities/{}/places".format(
                self.city.id), data="bad", follow_redirects=True)
            self.assertEqual(resp.status_code, 400)
            self.assertIn(b"Not a JSON", resp.data)

    def test_places_post_missing_name(self):
        """Test POST method with missing name in JSON on /places route."""
        with self.__app as a:
            resp = a.post("/api/v1/cities/{}/places".format(self.city.id),
                          json={"missing": "name", "user_id": self.user.id},
                          follow_redirects=True)
            self.assertEqual(resp.status_code, 400)
            self.assertIn(b"Missing name", resp.data)

    def test_places_post_missing_user_id(self):
        """Test POST method with missing user_id in JSON on /places route."""
        with self.__app as a:
            resp = a.post("/api/v1/cities/{}/places".format(self.city.id),
                          json={"name": "here", "missing": "user_id"},
                          follow_redirects=True)
            self.assertEqual(resp.status_code, 400)
            self.assertIn(b"Missing user_id", resp.data)

    def test_places_post_bad_city_id(self):
        """Test POST method with bad city_id in JSON on /places route."""
        with self.__app as a:
            resp = a.post("/api/v1/cities/bad/places", json={"name": "here"},
                          follow_redirects=True)
            self.assertEqual(resp.status_code, 404)

    def test_places_delete(self):
        """Test DELETE method on /places route."""
        place = Place(name="Stadium",
                      user_id=self.user.id, city_id=self.city.id)
        place.save()
        with self.__app as a:
            resp = a.delete("/api/v1/places/{}".format(place.id),
                            follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertDictEqual(resp.get_json(), {})
            self.assertNotIn(place, list(storage.all("Place").values()))

    def test_places_bad_delete(self):
        """Test DELETE method with nonexistant object on /places route."""
        with self.__app as a:
            resp = a.delete("/api/v1/places/bad", follow_redirects=True)
            self.assertEqual(resp.status_code, 404)

    def test_places_put(self):
        """Test PUT method on /places route."""
        with self.__app as a:
            data = {
                "name": "Attic",
                "id": "avoid",
                "user_id": "avoid",
                "city_id": "avoid",
                "created_at": "avoid",
                "updated_at": "avoid",
            }
            resp = a.put("/api/v1/places/{}".format(self.place.id),
                         json=data, follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.get_json().get("name"), "Attic")
            place = storage.get("Place", self.place.id)
            self.assertEqual(place.name, "Attic")
            self.assertNotEqual(place.id, "avoid")
            self.assertNotEqual(place.user_id, "avoid")
            self.assertNotEqual(place.city_id, "avoid")
            self.assertNotEqual(place.created_at, "avoid")
            self.assertNotEqual(place.updated_at, "avoid")

    def test_places_bad_put(self):
        """Test PUT method with invalid place on /places route."""
        with self.__app as a:
            resp = a.put("/api/v1/places/bad", follow_redirects=True)
            self.assertEqual(resp.status_code, 404)

    def test_places_bad_put_data(self):
        """Test PUT method with invalid JSON data on /places route."""
        with self.__app as a:
            resp = a.put("/api/v1/places/{}".format(self.place.id),
                         data="bad", follow_redirects=True)
            self.assertEqual(resp.status_code, 400)
            self.assertIn(b"Not a JSON", resp.data)

    def test_reviews_get(self):
        """Test GET method on /reviews route."""
        with self.__app as a:
            resp = a.get("/api/v1/places/{}/reviews".format(self.place.id),
                         follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn(storage.get("Review", self.review.id).to_dict(),
                          resp.get_json())

    def test_reviews_get_id(self):
        """Test GET method with specific id on /reviews route."""
        with self.__app as a:
            resp = a.get("/api/v1/reviews/{}".format(self.review.id),
                         follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(self.review.id, resp.get_json().get("id"))

    def test_reviews_post(self):
        """Test POST method on /reviews route."""
        with self.__app as a:
            data = {
                "text": "Alright",
                "user_id": self.user.id,
            }
            count = storage.count()
            resp = a.post("/api/v1/places/{}/reviews".format(self.place.id),
                          json=data, follow_redirects=True)
            msg = resp.get_json()
            self.assertEqual(resp.status_code, 201)
            self.assertEqual(msg.get("__class__"), "Review")
            self.assertEqual(msg.get("text"), "Alright")
            self.assertGreater(storage.count(), count)

    def test_reviews_bad_post(self):
        """Test POST method with bad JSON format on /reviews route."""
        with self.__app as a:
            resp = a.post("/api/v1/places/{}/reviews".format(
                self.place.id), data="bad", follow_redirects=True)
            self.assertEqual(resp.status_code, 400)
            self.assertIn(b"Not a JSON", resp.data)

    def test_reviews_post_missing_text(self):
        """Test POST method with missing text in JSON on /reviews route."""
        with self.__app as a:
            resp = a.post("/api/v1/places/{}/reviews".format(self.place.id),
                          json={"missing": "text", "user_id": self.user.id},
                          follow_redirects=True)
            self.assertEqual(resp.status_code, 400)
            self.assertIn(b"Missing text", resp.data)

    def test_reviews_post_missing_user_id(self):
        """Test POST method with missing text in JSON on /reviews route."""
        with self.__app as a:
            resp = a.post("/api/v1/places/{}/reviews".format(self.place.id),
                          json={"text": "here", "missing": "user_id"},
                          follow_redirects=True)
            self.assertEqual(resp.status_code, 400)
            self.assertIn(b"Missing user_id", resp.data)

    def test_reviews_post_bad_place(self):
        """Test POST method with missing text in JSON on /reviews route."""
        with self.__app as a:
            resp = a.post("/api/v1/places/bad/reviews", json={"tmp": "tmp"},
                          follow_redirects=True)
            self.assertEqual(resp.status_code, 404)

    def test_reviews_delete(self):
        """Test DELETE method on /reviews route."""
        review = Review(text="Eh", user_id=self.user.id,
                        place_id=self.place.id)
        review.save()
        with self.__app as a:
            resp = a.delete("/api/v1/reviews/{}".format(review.id),
                            follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertDictEqual(resp.get_json(), {})
            self.assertNotIn(review, list(storage.all("Review").values()))

    def test_reviews_bad_delete(self):
        """Test DELETE method with nonexistant object on /reviews route."""
        with self.__app as a:
            resp = a.delete("/api/v1/reviews/bad", follow_redirects=True)
            self.assertEqual(resp.status_code, 404)

    def test_reviews_put(self):
        """Test PUT method on /reviews route."""
        with self.__app as a:
            data = {
                "text": "Updated",
                "id": "avoid",
                "user_id": "avoid",
                "place_id": "avoid",
                "created_at": "avoid",
                "updated_at": "avoid",
            }
            resp = a.put("/api/v1/reviews/{}".format(self.review.id),
                         json=data, follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.get_json().get("text"), "Updated")
            review = storage.get("Review", self.review.id)
            self.assertEqual(review.text, "Updated")
            self.assertNotEqual(review.id, "avoid")
            self.assertNotEqual(review.user_id, "avoid")
            self.assertNotEqual(review.place_id, "avoid")
            self.assertNotEqual(review.created_at, "avoid")
            self.assertNotEqual(review.updated_at, "avoid")

    def test_reviews_bad_put(self):
        """Test PUT method with invalid review on /reviews route."""
        with self.__app as a:
            resp = a.put("/api/v1/reviews/bad", follow_redirects=True)
            self.assertEqual(resp.status_code, 404)

    def test_reviews_bad_put_data(self):
        """Test PUT method with invalid JSON data on /reviews route."""
        with self.__app as a:
            resp = a.put("/api/v1/reviews/{}".format(self.review.id),
                         data="bad", follow_redirects=True)
            self.assertEqual(resp.status_code, 400)
            self.assertIn(b"Not a JSON", resp.data)

    def test_places_amenities_get(self):
        """Test GET with specific places id"""
        with self.__app as a:
            resp = a.get("/api/v1/places/{}/amenities".format(self.place.id))
            self.assertEqual(resp.status_code, 200)

    def test_places_amenities_bad_get(self):
        """Test bad GET with specific places id"""
        with self.__app as a:
            resp = a.get("/api/v1/places/{}/amenities".format("bad_id"))
            self.assertEqual(resp.status_code, 404)

    def test_places_amenities_new_post(self):
        """Test a POST a valid amenity that doesn't exists for the places"""
        with self.__app as a:
            amenity = Amenity(name="free money")
            amenity.save()
            resp = a.post("/api/v1/places/{}/amenities/{}".format(
                self.place.id,
                amenity.id
            ))
            self.assertEqual(resp.status_code, 201)

    def test_places_amenities_exists_post(self):
        """Test a POST a valid amenity that exists for the places"""
        with self.__app as a:
            resp = a.post("/api/v1/places/{}/amenities/{}".format(
                self.place.id,
                self.amenity_2.id
            ))
            self.assertEqual(resp.status_code, 200)

    def test_places_amenities_new_post_bad_amenity(self):
        """Test a POST a invalid amenity that doesn't exists for the places"""
        with self.__app as a:
            resp = a.post("/api/v1/places/{}/amenities/{}".format(
                self.place.id,
                "bad_id"
            ))
            self.assertEqual(resp.status_code, 404)

    def test_places_amenities_new_post_bad_place(self):
        """Test a POST a invalid places id"""
        with self.__app as a:
            resp = a.post("/api/v1/places/{}/amenities/{}".format(
                "bad_id",
                self.amenity_2.id
            ))
            self.assertEqual(resp.status_code, 404)

    # DELETE
    def test_places_amenities_bad_delete(self):
        """Test a DELETE a invalid amenity
        that doesn't exists for the places
        """
        with self.__app as a:
            amenity = Amenity(name="monty python")
            amenity.save()
            resp = a.delete("/api/v1/places/{}/amenities/{}".format(
                self.place.id,
                amenity.id
            ))
            self.assertEqual(resp.status_code, 404)

    def test_places_amenities_delete(self):
        """Test a DELETE a valid amenity that exists for the places"""
        with self.__app as a:
            resp = a.post("/api/v1/places/{}/amenities/{}".format(
                self.place.id,
                self.amenity_2.id
            ))
            self.assertEqual(resp.status_code, 200)

    def test_places_amenities_delete_bad_amenity(self):
        """Test a DELETE a invalid amenity
        that doesn't exists for the places
        """
        with self.__app as a:
            resp = a.post("/api/v1/places/{}/amenities/{}".format(
                self.place.id,
                "bad_id"
            ))
            self.assertEqual(resp.status_code, 404)

    def test_places_amenities_delete_bad_place(self):
        """Test a DELETE a invalid places id"""
        with self.__app as a:
            resp = a.post("/api/v1/places/{}/amenities/{}".format(
                "bad_id",
                self.amenity_2.id
            ))
            self.assertEqual(resp.status_code, 404)


if __name__ == "__main__":
    unittest.main()
