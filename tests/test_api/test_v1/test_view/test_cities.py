#!/usr/bin/python3
"""
Testing cities.py file
"""
from api.v1.app import (app)
import flask
import json
from models import storage
from models.city import City
from models.state import State
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
        """set the flask app in testing mode - create a state to test cities"""
        app.config['TESTING'] = True
        cls.app = app.test_client()
        cls.path = "/api/v1"
        cls.state_args = {"name": "Botswana", "id": "BO"}
        cls.state = State(**cls.state_args)
        cls.state.save()

    @classmethod
    def tearDownClass(cls):
        storage.delete(cls.state)

    def test_getcities(self):
        """test listing all cities"""
        city_args = {"name": "Gaborone", "id": "GA", "state_id": "BO"}
        city = City(**city_args)
        city.save()
        rv = self.app.get('{}/states/{}/cities'.format(
            self.path, self.state.id),
                          follow_redirects=True)
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.headers.get("Content-Type"), "application/json")
        json_format = getJson(rv)
        self.assertTrue(type(json_format), list)
        self.assertIn(city_args["name"], [e.get("name") for e in json_format])
        storage.delete(city)

    def test_getcities_badstate(self):
        """test listing all cities with a bad state id"""
        city_args = {"name": "Gaborone", "id": "GA", "state_id": "BO"}
        city = City(**city_args)
        city.save()
        rv = self.app.get('{}/states/{}/cities'.format(self.path, "noID"),
                          follow_redirects=True)
        self.assertEqual(rv.status_code, 404)
        storage.delete(city)

    def test_view_one_city(self):
        """test retrieving one state"""
        city_args = {"name": "Gaborone", "id": "GA", "state_id": "BO"}
        city = City(**city_args)
        city.save()
        rv = self.app.get('{}/cities/{}'.format(self.path, city_args["id"]),
                          follow_redirects=True)
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.headers.get("Content-Type"), "application/json")
        json_format = getJson(rv)
        self.assertEqual(json_format.get("name"), city_args["name"])
        self.assertEqual(json_format.get("id"), city_args["id"])
        storage.delete(city)

    def test_view_one_city_wrong(self):
        """the id does not match a city"""
        city_args = {"name": "Gaborone", "id": "GA", "state_id": "BO"}
        city = City(**city_args)
        city.save()
        rv = self.app.get('{}/cities/{}/'.format(self.path, "noID"),
                          follow_redirects=True)
        self.assertEqual(rv.status_code, 404)
        storage.delete(city)

    def test_delete_city(self):
        """test delete a city"""
        city_args = {"name": "Gaborone", "id": "GA", "state_id": "BO"}
        city = City(**city_args)
        city.save()
        rv = self.app.delete('{}/cities/{}/'.format(self.path,
                                                    city_args["id"]),
                             follow_redirects=True)
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.headers.get("Content-Type"), "application/json")
        json_format = getJson(rv)
        self.assertEqual(json_format, {})
        self.assertIsNone(storage.get("City", city_args["id"]))

    def test_delete_city_wrong(self):
        """the id does not match a city"""
        city_args = {"name": "Gaborone", "id": "GA", "state_id": "BO"}
        city = City(**city_args)
        city.save()
        rv = self.app.delete('{}/cities/{}/'.format(self.path, "noID"),
                             follow_redirects=True)
        self.assertEqual(rv.status_code, 404)
        storage.delete(city)

    def test_create_city(self):
        """test creating a city"""
        city_args = {"name": "Gaborone", "id": "GA"}
        rv = self.app.post('{}/states/{}/cities/'.format(
            self.path, self.state.id),
                           content_type="application/json",
                           data=json.dumps(city_args),
                           follow_redirects=True)
        self.assertEqual(rv.status_code, 201)
        self.assertEqual(rv.headers.get("Content-Type"), "application/json")
        json_format = getJson(rv)
        self.assertEqual(json_format.get("name"), city_args["name"])
        self.assertEqual(json_format.get("id"), city_args["id"])
        s = storage.get("City", city_args["id"])
        self.assertIsNotNone(s)
        storage.delete(s)

    def test_create_city_bad_json(self):
        """test creating a city with invalid json"""
        city_args = {"name": "Gaborone", "id": "GA"}
        rv = self.app.post('{}/states/{}/cities/'.format(
            self.path, self.state.id),
                           content_type="application/json",
                           data=city_args,
                           follow_redirects=True)
        self.assertEqual(rv.status_code, 400)
        self.assertEqual(rv.get_data(), b"Not a JSON")

    def test_create_city_no_name(self):
        """test creating a city without a name"""
        city_args = {"id": "ZA2"}
        rv = self.app.post('{}/states/{}/cities/'.format(
            self.path, self.state.id),
                           content_type="application/json",
                           data=json.dumps(city_args),
                           follow_redirects=True)
        self.assertEqual(rv.status_code, 400)
        self.assertEqual(rv.get_data(), b"Missing name")

    def test_create_city_bad_stateid(self):
        """test creating a city with not matching state"""
        city_args = {"name": "Gaborone", "id": "ZA2"}
        rv = self.app.post('{}/states/{}/cities/'.format(
            self.path, "noID"),
                           content_type="application/json",
                           data=json.dumps(city_args),
                           follow_redirects=True)
        self.assertEqual(rv.status_code, 404)

    def test_update_city_name(self):
        """test updating a city"""
        city_args = {"name": "Gaborone", "id": "GA", "state_id": "BO"}
        city = City(**city_args)
        city.save()
        rv = self.app.put('{}/cities/{}/'.format(self.path, city.id),
                          content_type="application/json",
                          data=json.dumps({"name": "Z"}),
                          follow_redirects=True)
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.headers.get("Content-Type"), "application/json")
        json_format = getJson(rv)
        self.assertEqual(json_format.get("name"), "Z")
        self.assertEqual(json_format.get("id"), city_args["id"])
        self.assertEqual(json_format.get("state_id"), city_args["state_id"])
        storage.delete(city)

    def test_update_city_id(self):
        """test cannot update city id"""
        city_args = {"name": "Gaborone", "id": "GA", "state_id": "BO"}
        city = City(**city_args)
        city.save()
        rv = self.app.put('{}/cities/{}/'.format(self.path, city.id),
                          content_type="application/json",
                          data=json.dumps({"id": "Z"}),
                          follow_redirects=True)
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.headers.get("Content-Type"), "application/json")
        json_format = getJson(rv)
        self.assertEqual(json_format.get("name"), city_args["name"])
        self.assertEqual(json_format.get("id"), city_args["id"])
        self.assertEqual(json_format.get("state_id"), city_args["state_id"])
        storage.delete(city)

    def test_update_city_state_id(self):
        """test cannot update city state_id"""
        city_args = {"name": "Gaborone", "id": "GA", "state_id": "BO"}
        city = City(**city_args)
        city.save()
        rv = self.app.put('{}/cities/{}/'.format(self.path, city.id),
                          content_type="application/json",
                          data=json.dumps({"state_id": "Z"}),
                          follow_redirects=True)
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.headers.get("Content-Type"), "application/json")
        json_format = getJson(rv)
        self.assertEqual(json_format.get("name"), city_args["name"])
        self.assertEqual(json_format.get("id"), city_args["id"])
        self.assertEqual(json_format.get("state_id"), city_args["state_id"])
        storage.delete(city)

    def test_update_city_bad_json(self):
        """test update with ill formedt json"""
        city_args = {"name": "Gaborone", "id": "GA", "state_id": "BO"}
        city = City(**city_args)
        city.save()
        rv = self.app.put('{}/cities/{}/'.format(self.path, city.id),
                          content_type="application/json",
                          data={"id": "Z"},
                          follow_redirects=True)
        self.assertEqual(rv.status_code, 400)
        self.assertEqual(rv.get_data(), b"Not a JSON")
        storage.delete(city)

    def test_update_city_bad_id(self):
        """test update with no matching id"""
        city_args = {"name": "Gaborone", "id": "GA", "state_id": "BO"}
        city = City(**city_args)
        city.save()
        rv = self.app.put('{}/cities/{}/'.format(self.path, "noID"),
                          content_type="application/json",
                          data=json.dumps({"name": "Z"}),
                          follow_redirects=True)
        self.assertEqual(rv.status_code, 404)
        storage.delete(city)


if __name__ == "__main__":
    unittest.main()
