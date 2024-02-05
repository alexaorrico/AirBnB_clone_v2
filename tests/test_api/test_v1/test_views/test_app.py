#!/usr/bin/python3
""" Functions to test whethher json givin response"""
import unittest
from api.v1.app import app
import os
from models.state import State
from models.city import City
from models.place import Place
from models.user import User
from models import storage
import uuid
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError


class TestStatus(unittest.TestCase):
    """ This class tests the status behaviour of
    the api"""
    def setUp(self):
        """ Set up method"""
        self.ctx = app.app_context()
        self.ctx.push()
        self.client = app.test_client()

    def tearDown(self):
        """Tear down app context """
        self.ctx.pop()

    def test_status_ok(self):
        """ Check for status"""
        with app.test_client() as c:
            rv = c.get("/api/v1/status")
            json_data = rv.get_json()
            self.assertDictEqual(
                    json_data,
                    {"status": "OK"}
                    )

    def test_response_code(self):
        """ Test for the response code"""
        with app.test_client() as c:
            rv = c.get("/api/v1/status")
            self.assertEqual(rv.status_code, 200)


class TestError404(unittest.TestCase):
    """ This class tests for error404"""
    def test_response_code(self):
        """ Test for the response code"""
        with app.test_client() as c:
            rv = c.get("/api/v1/doesnotexist")
            self.assertEqual(rv.status_code, 404)

    def test_error_404(self):
        """ Test the error object itself"""
        with app.test_client() as c:
            rv = c.get("/api/v1/doesnotexist")
            json_data = rv.get_json()
            self.assertDictEqual(
                    json_data,
                    {"error": "Not found"}
                    )


@unittest.skipIf(os.getenv("HBNB_MYSQL_DB") == "hbnb_dev_db", "Dev db")
class TestCityViews(unittest.TestCase):
    """ This class tests for city views"""
    def tearDown(self):
        """Tear down context """
        if (os.getenv("HBNB_TYPE_STORAGE") == "db"):
            storage.delete(self.ondo_state_object)
            # Place.__table__.drop(bind=storage._DBStorage__engine)
            # City.__table__.drop(bind=storage._DBStorage__engine)
            # State.__table__.drop(bind=storage._DBStorage__engine)
            storage.save()
        else:
            os.remove("file.json")

    def setUp(self):
        """ Set up context """
        try:
            self.ondo_state_object = State()
            setattr(self.ondo_state_object, "name", "Ondo")
            self.owo_city_object = City(**{
                    "name": "Owo",
                    "state_id": self.ondo_state_object.id,
                    "id": str(uuid.uuid4()),
                    "created_at": datetime.now(),
                    "updated_at": datetime.now()
                    })
            self.akure_city_object = City(**{
                    "name": "Akure",
                    "state_id": self.ondo_state_object.id,
                    "id": str(uuid.uuid4()),
                    "created_at": datetime.now(),
                    "updated_at": datetime.now()
                    })
            storage.new(self.ondo_state_object)
            storage.new(self.owo_city_object)
            storage.new(self.akure_city_object)
            storage.save()
        except (SQLAlchemyError):
            storage.delete(self.ondo_state_object)
            storag.save()
            # City.__table__.drop()
            # State.__table__.drop()

    def test_views_get_cities(self):
        """ Test for get for valid cities id """
        with app.test_client() as c:
            ondo_state_id = self.ondo_state_object.id
            rv = c.get(f'/api/v1/states/{ondo_state_id}/cities')
            expected_json_list = rv.get_json()
            self.assertEqual(
                len(expected_json_list), 2,
                "Ondo cities != 2"
                )
            owo_id = self.owo_city_object.id
            expected_city_ids = [
                        city["id"] for city in expected_json_list
                        ]
            self.assertIn(
                    self.owo_city_object.id,
                    expected_city_ids
                    )
            self.assertEqual(rv.status_code, 200)

    def test_get_cities_invalid_id(self):
        """ Test with invalid id """
        with app.test_client() as c:
            rv = c.get("/api/v1/states/invalid_id/cities")
            self.assertDictEqual(
                    rv.get_json(),
                    {"error": "Not found"}
                    )
            self.assertEqual(rv.status_code, 404)

    def test_views_get_city(self):
        """ Test for get valid city_id """
        with app.test_client() as c:
            akure_city_id = self.akure_city_object.id
            rv = c.get(f'/api/v1/cities/{akure_city_id}')
            expected_json_repr = rv.get_json()
            self.assertDictEqual(
                    expected_json_repr,
                    self.akure_city_object.to_dict()
                )
            self.assertEqual(rv.status_code, 200)

    def test_get_city_invalid_id(self):
        """ Testing with invalid city_id"""
        with app.test_client() as c:
            rv = c.get('/api/v1/cities/invalid_id')
            self.assertEqual(rv.status_code, 404)
            self.assertDictEqual(
                    rv.get_json(),
                    {"error": "Not found"}
                    )

    def test_delete_city(self):
        """ Test the DELETE option on a given valid
        city_id"""
        akure_city_id = self.akure_city_object.id
        with app.test_client() as c:
            rv = c.delete(f'/api/v1/cities/{akure_city_id}')
            self.assertDictEqual(
                        rv.get_json(),
                        {}
                        )
            self.assertEqual(rv.status_code, 200)
        #  After deletion, akure_city_id should be invalid.
        with app.test_client() as c:
            rv = c.delete(f'/api/v1/cities/{akure_city_id}')
            self.assertEqual(404, rv.status_code)
            self.assertDictEqual(
                        {"error": "Not found"},
                        rv.get_json()
                        )

    def test_post_cites(self):
        """ This will test for behaviours for
        when a new city object is posted to cities"""
        ondo_id = self.ondo_state_object.id
        with app.test_client() as c:
            rv = c.post(
                    "/api/v1/states/invalidstateid/cities",
                    json={
                        "name": "Akoko",
                        "id": str(uuid.uuid4()),
                        "created_at": datetime.now(),
                        "updated_at": datetime.now()
                        }
                    )
            self.assertEqual(404, rv.status_code)
        #  Pass in some html data
        with app.test_client() as c:
            rv = c.post(
                    f"/api/v1/states/{ondo_id}/cities",
                    data='<html>lang=en-us</html>'
                    )
            self.assertEqual(400, rv.status_code)
        #  Remove the use of name in json data
        with app.test_client() as c:
            rv = c.post(
                    f"/api/v1/states/{ondo_id}/cities",
                    json={
                        "id": str(uuid.uuid4()),
                        "created_at": datetime.now(),
                        "updated_at": datetime.now()
                        }
                    )
            self.assertEqual(400, rv.status_code)
        #  Correct POST request.
        with app.test_client() as c:
            rv = c.post(
                    f"/api/v1/states/{ondo_id}/cities",
                    json={
                        "name": "Akoko",
                        "id": str(uuid.uuid4()),
                        "created_at": datetime.now().strftime(
                                "%Y-%m-%dT%H:%M:%S.%f"
                                ),
                        "updated_at": datetime.now().strftime(
                                "%Y-%m-%dT%H:%M:%S.%f"
                                )
                        }
                    )
            self.assertEqual(201, rv.status_code)
            expected_akoko_object = City(**{
                    "name": "Akoko",
                    "state_id": self.ondo_state_object.id,
                    "id": str(uuid.uuid4()),
                    "created_at": datetime.now(),
                    "updated_at": datetime.now()
                    })
            self.assertEqual(
                    rv.get_json()["name"],
                    "Akoko"
                        )
            self.assertEqual(
                    rv.get_json().get("state_id", None),
                    ondo_id
                        )
            self.assertGreaterEqual(
                        len(rv.get_json()["id"]),
                        28
                        )
            self.assertEqual(
                        len(rv.get_json()["created_at"]),
                        len(rv.get_json()["updated_at"])
                        )


@unittest.skipIf(os.getenv("HBNB_MYSQL_DB") == "hbnb_dev_db", "Dev db")
class TestUserViews(unittest.TestCase):
    """ This class tests for user views"""
    def tearDown(self):
        """Tear down context """
        if (os.getenv("HBNB_TYPE_STORAGE") == "db"):
            storage.delete(self.akingbeni_user_object)
            storage.delete(self.david_user_object)
            storage.save()
        else:
            os.remove("file.json")

    def setUp(self):
        """ Set up context """
        try:
            self.akingbeni_user_object = User(**{
                    "email": "xyz@mail.com",
                    "password": "xyz",
                    "first_name": "akingbeni",
                    "last_name": "akin"
                    })
            #  setattr(self.akingbeni_user_object, "name", "Akingbeni")
            self.david_user_object = User(**{
                    "email": "abc@mail.com",
                    "password": "123",
                    "first_name": "david",
                    "last_name": "dave"
                    })
            #  setattr(self.david_user_object, "name", "David")
            storage.new(self.akingbeni_user_object)
            storage.new(self.david_user_object)
            storage.save()
        except (SQLAlchemyError):
            storage.delete(self.akingbeni_user_object)
            storage.delete(self.david_user_object)
            storage.save()

    def test_views_get_users(self):
        """ Test for get for users"""
        with app.test_client() as c:
            rv = c.get(f'/api/v1/users')
            output_json_list = rv.get_json()
            self.assertEqual(
                len(output_json_list), 3,
                "Users != 3"
                )
