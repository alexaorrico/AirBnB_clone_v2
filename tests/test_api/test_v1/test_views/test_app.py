#!/usr/bin/python3
""" Functions to test whethher json givin response"""
import unittest
from api.v1.app import app
import os
from models.state import State
from models.city import City
from models.place import Place
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
