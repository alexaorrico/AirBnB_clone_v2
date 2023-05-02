#!/usr/bin/python3
"""
Testing places.py file
"""
from api.v1.app import (app)
import flask
import json
from models import storage
from models.city import City
from models.place import Place
from models.state import State
from models.user import User
import unittest


def getJson(response):
    """
    Extract the json dictionary from a flask Response object

    Argument:
        response: a reponse object from Flask

    Return:
        a dictionary or None or maybe raise an exception
    """
    return json.loads(str(response.get_data(), encoding="utf-8"))


class TestCityView(unittest.TestCase):
    """Test all routes in cities.py"""

    @classmethod
    def setUpClass(cls):
        """
        set the flask app in testing mode
        create a state, city, user to test places
        """
        app.config['TESTING'] = True
        cls.app = app.test_client()
        cls.path = "/api/v1"
        cls.state_args = {"name": "Botswana", "id": "BO"}
        cls.state = State(**cls.state_args)
        cls.state.save()
        cls.city_args = {"name": "Gaborone", "id": "GA",
                         "state_id": cls.state.id}
        cls.city = City(**cls.city_args)
        cls.city.save()
        cls.user_args = {"email": "a@b.com", "password": "1234",
                         "id": "U1"}
        cls.user = User(**cls.user_args)
        cls.user.save()

    @classmethod
    def tearDownClass(cls):
        """remove created objects"""
        storage.delete(cls.state)
        storage.delete(cls.user)

    def test_getplaces(self):
        """test listing all places in a city"""
        place_args = {"name": "cage", "city_id": self.city.id,
                      "user_id": self.user.id}
        place = Place(**place_args)
        place.save()
        rv = self.app.get('{}/cities/{}/places'.format(
            self.path, self.city.id),
                          follow_redirects=True)
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.headers.get("Content-Type"), "application/json")
        json_format = getJson(rv)
        self.assertTrue(type(json_format), list)
        self.assertIn(place_args["name"], [e.get("name") for e in json_format])
        self.assertIn(place_args["user_id"],
                      [e.get("user_id") for e in json_format])
        storage.delete(place)

    def test_getplaces_bad_city(self):
        """test listing all places with a bad city id"""
        place_args = {"name": "cage", "city_id": self.city.id,
                      "user_id": self.user.id}
        place = Place(**place_args)
        place.save()
        rv = self.app.get('{}/cities/{}/places'.format(self.path, "noID"),
                          follow_redirects=True)
        self.assertEqual(rv.status_code, 404)
        storage.delete(place)

    def test_view_one_place(self):
        """test retrieving one place"""
        place_args = {"name": "cage", "city_id": self.city.id,
                      "user_id": self.user.id, "id": "CA"}
        place = Place(**place_args)
        place.save()
        rv = self.app.get('{}/places/{}'.format(self.path, place_args["id"]),
                          follow_redirects=True)
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.headers.get("Content-Type"), "application/json")
        json_format = getJson(rv)
        self.assertEqual(json_format.get("name"), place_args["name"])
        self.assertEqual(json_format.get("id"), place_args["id"])
        self.assertEqual(json_format.get("user_id"), place_args["user_id"])
        storage.delete(place)

    def test_view_one_place_wrong(self):
        """the id does not match a place"""
        place_args = {"name": "cage", "city_id": self.city.id,
                      "user_id": self.user.id, "id": "CA"}
        place = Place(**place_args)
        place.save()
        rv = self.app.get('{}/places/{}/'.format(self.path, "noID"),
                          follow_redirects=True)
        self.assertEqual(rv.status_code, 404)
        storage.delete(place)

    def test_delete_place(self):
        """test delete a place"""
        place_args = {"name": "cage", "city_id": self.city.id,
                      "user_id": self.user.id, "id": "CA"}
        place = Place(**place_args)
        place.save()
        rv = self.app.delete('{}/places/{}/'.format(self.path,
                                                    place_args["id"]),
                             follow_redirects=True)
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.headers.get("Content-Type"), "application/json")
        json_format = getJson(rv)
        self.assertEqual(json_format, {})
        self.assertIsNone(storage.get("Place", place_args["id"]))

    def test_delete_place_wrong(self):
        """the id does not match a place"""
        place_args = {"name": "cage", "city_id": self.city.id,
                      "user_id": self.user.id, "id": "CA"}
        place = Place(**place_args)
        place.save()
        rv = self.app.delete('{}/places/{}/'.format(self.path, "noID"),
                             follow_redirects=True)
        self.assertEqual(rv.status_code, 404)
        storage.delete(place)

    def test_create_place(self):
        """test creating a place"""
        place_args = {"name": "cage",
                      "user_id": self.user.id, "id": "CA"}
        rv = self.app.post('{}/cities/{}/places/'.format(self.path,
                                                         self.city.id),
                           content_type="application/json",
                           data=json.dumps(place_args),
                           follow_redirects=True)
        self.assertEqual(rv.status_code, 201)
        self.assertEqual(rv.headers.get("Content-Type"), "application/json")
        json_format = getJson(rv)
        self.assertEqual(json_format.get("name"), place_args["name"])
        self.assertEqual(json_format.get("id"), place_args["id"])
        s = storage.get("Place", place_args["id"])
        self.assertIsNotNone(s)
        self.assertEqual(s.user_id, place_args["user_id"])
        storage.delete(s)

    def test_create_place_bad_json(self):
        """test creating a place with invalid json"""
        place_args = {"name": "cage",
                      "user_id": self.user.id, "id": "CA"}
        rv = self.app.post('{}/cities/{}/places/'.format(self.path,
                                                         self.city.id),
                           content_type="application/json",
                           data=place_args,
                           follow_redirects=True)
        self.assertEqual(rv.status_code, 400)
        self.assertEqual(rv.get_data(), b"Not a JSON")

    def test_create_place_no_name(self):
        """test creating a place without a name"""
        place_args = {"user_id": self.user.id, "id": "CA"}
        rv = self.app.post('{}/cities/{}/places/'.format(
            self.path, self.city.id),
                           content_type="application/json",
                           data=json.dumps(place_args),
                           follow_redirects=True)
        self.assertEqual(rv.status_code, 400)
        self.assertEqual(rv.get_data(), b"Missing name")

    def test_create_place_no_user_id(self):
        """test creating a place without a user_id"""
        place_args = {"name": "cage", "id": "CA"}
        rv = self.app.post('{}/cities/{}/places/'.format(
            self.path, self.city.id),
                           content_type="application/json",
                           data=json.dumps(place_args),
                           follow_redirects=True)
        self.assertEqual(rv.status_code, 400)
        self.assertEqual(rv.get_data(), b"Missing user_id")

    def test_create_place_bad_user_id(self):
        """test creating a place without a valid user_id"""
        place_args = {"name": "cage", "user_id": "noID", "id": "CA"}
        rv = self.app.post('{}/cities/{}/places/'.format(
            self.path, self.city.id),
                           content_type="application/json",
                           data=json.dumps(place_args),
                           follow_redirects=True)
        self.assertEqual(rv.status_code, 404)

    def test_create_place_bad_city_id(self):
        """test creating a city with not matching state"""
        place_args = {"name": "cage", "user_id": "noID", "id": "CA"}
        rv = self.app.post('{}/cities/{}/places/'.format(
            self.path, "noID"),
                           content_type="application/json",
                           data=json.dumps(place_args),
                           follow_redirects=True)
        self.assertEqual(rv.status_code, 404)

    def test_update_place_name(self):
        """test updating a place"""
        place_args = {"name": "cage", "city_id": self.city.id,
                      "user_id": self.user.id, "id": "CA"}
        place = Place(**place_args)
        place.save()
        rv = self.app.put('{}/places/{}/'.format(self.path, place.id),
                          content_type="application/json",
                          data=json.dumps({"name": "Z"}),
                          follow_redirects=True)
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.headers.get("Content-Type"), "application/json")
        json_format = getJson(rv)
        self.assertEqual(json_format.get("name"), "Z")
        self.assertEqual(json_format.get("id"), place_args["id"])
        self.assertEqual(json_format.get("user_id"), place_args["user_id"])
        self.assertEqual(json_format.get("city_id"), place_args["city_id"])
        storage.delete(place)

    def test_update_place_id(self):
        """test cannot update place id"""
        place_args = {"name": "cage", "city_id": self.city.id,
                      "user_id": self.user.id, "id": "CA"}
        place = Place(**place_args)
        place.save()
        rv = self.app.put('{}/places/{}/'.format(self.path, place.id),
                          content_type="application/json",
                          data=json.dumps({"id": "Z"}),
                          follow_redirects=True)
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.headers.get("Content-Type"), "application/json")
        json_format = getJson(rv)
        self.assertEqual(json_format.get("name"), place_args["name"])
        self.assertEqual(json_format.get("id"), place_args["id"])
        self.assertEqual(json_format.get("city_id"), place_args["city_id"])
        self.assertEqual(json_format.get("user_id"), place_args["user_id"])
        storage.delete(place)

    def test_update_place_city_id(self):
        """test cannot update place city_id"""
        place_args = {"name": "cage", "city_id": self.city.id,
                      "user_id": self.user.id, "id": "CA"}
        place = Place(**place_args)
        place.save()
        rv = self.app.put('{}/places/{}/'.format(self.path, place.id),
                          content_type="application/json",
                          data=json.dumps({"city_id": "Z"}),
                          follow_redirects=True)
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.headers.get("Content-Type"), "application/json")
        json_format = getJson(rv)
        self.assertEqual(json_format.get("name"), place_args["name"])
        self.assertEqual(json_format.get("id"), place_args["id"])
        self.assertEqual(json_format.get("city_id"), place_args["city_id"])
        self.assertEqual(json_format.get("user_id"), place_args["user_id"])
        storage.delete(place)

    def test_update_place_user_id(self):
        """test cannot update place user_id"""
        place_args = {"name": "cage", "city_id": self.city.id,
                      "user_id": self.user.id, "id": "CA"}
        place = Place(**place_args)
        place.save()
        rv = self.app.put('{}/places/{}/'.format(self.path, place.id),
                          content_type="application/json",
                          data=json.dumps({"user_id": "Z"}),
                          follow_redirects=True)
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.headers.get("Content-Type"), "application/json")
        json_format = getJson(rv)
        self.assertEqual(json_format.get("name"), place_args["name"])
        self.assertEqual(json_format.get("id"), place_args["id"])
        self.assertEqual(json_format.get("city_id"), place_args["city_id"])
        self.assertEqual(json_format.get("user_id"), place_args["user_id"])
        storage.delete(place)

    def test_update_place_bad_json(self):
        """test update with ill formed json"""
        place_args = {"name": "cage", "city_id": self.city.id,
                      "user_id": self.user.id, "id": "CA"}
        place = Place(**place_args)
        place.save()
        rv = self.app.put('{}/places/{}/'.format(self.path, place.id),
                          content_type="application/json",
                          data={"id": "Z"},
                          follow_redirects=True)
        self.assertEqual(rv.status_code, 400)
        self.assertEqual(rv.get_data(), b"Not a JSON")
        storage.delete(place)

    def test_update_city_bad_id(self):
        """test update with no matching id"""
        place_args = {"name": "cage", "city_id": self.city.id,
                      "user_id": self.user.id, "id": "CA"}
        place = Place(**place_args)
        place.save()
        rv = self.app.put('{}/places/{}/'.format(self.path, "noID"),
                          content_type="application/json",
                          data=json.dumps({"name": "Z"}),
                          follow_redirects=True)
        self.assertEqual(rv.status_code, 404)
        storage.delete(place)


if __name__ == "__main__":
    unittest.main()
