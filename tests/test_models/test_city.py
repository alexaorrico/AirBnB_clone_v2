#!/usr/bin/python3
"""
Contains the TestCityDocs classes
"""

from datetime import datetime
import inspect
import models
from models import city
from models.city import City
from models.base_model import BaseModel
import pep8
import unittest
from os import getenv
import MySQLdb


class TestCityDocs(unittest.TestCase):
    """Tests to check the documentation and style of City class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.city_f = inspect.getmembers(City, inspect.isfunction)

    def test_pep8_conformance_city(self):
        """Test that models/city.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/city.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_city(self):
        """Test that tests/test_models/test_city.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_city.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_city_module_docstring(self):
        """Test for the city.py module docstring"""
        self.assertIsNot(city.__doc__, None,
                         "city.py needs a docstring")
        self.assertTrue(len(city.__doc__) >= 1,
                        "city.py needs a docstring")

    def test_city_class_docstring(self):
        """Test for the City class docstring"""
        self.assertIsNot(City.__doc__, None,
                         "City class needs a docstring")
        self.assertTrue(len(City.__doc__) >= 1,
                        "City class needs a docstring")

    def test_city_func_docstrings(self):
        """Test for the presence of docstrings in City methods"""
        for func in self.city_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestCity(unittest.TestCase):
    """Test the City class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        if models.storage_t == 'db':
            """
            TestCity.HBNB_MYSQL_USER = getenv('HBNB_MYSQL_USER')
            TestCity.HBNB_MYSQL_PWD = getenv('HBNB_MYSQL_PWD')
            TestCity.HBNB_MYSQL_HOST = getenv('HBNB_MYSQL_HOST')
            TestCity.HBNB_MYSQL_DB = getenv('HBNB_MYSQL_DB')

            TestCity.db_conn = MySQLdb.connect(
                user=TestCity.HBNB_MYSQL_USER,
                password=TestCity.HBNB_MYSQL_PWD,
                host=TestCity.HBNB_MYSQL_HOST,
                database=TestCity.HBNB_MYSQL_DB)
            """
            pass

    @classmethod
    def tearDownClass(cls):
        """Close database connections"""
        if models.storage_t == 'db':
            pass

    def setUp(self):
        """Setup database for each testcase"""
        if models.storage_t == 'db':
            pass

    def test_is_subclass(self):
        """Test that City is a subclass of BaseModel"""
        city = City()
        self.assertIsInstance(city, BaseModel)
        self.assertTrue(hasattr(city, "id"))
        self.assertTrue(hasattr(city, "created_at"))
        self.assertTrue(hasattr(city, "updated_at"))

    def test_instantiation_with_kwargs(self):
        """Test that the object is correctly created using **kwargs"""
        kwargs = dict(
            name="Holbertonland",
            state_id="123f332d-acf12-149f-13298f2f3f2")
        state_id = "123f332d-acf12-149f-13298f2f3f2"
        tic = datetime.utcnow()
        inst = City(**kwargs)
        toc = datetime.utcnow()
        attrs_types = {
            "id": str,
            "created_at": datetime,
            "updated_at": datetime,
            "name": str,
            "state_id": str
        }
        for attr, typ in attrs_types.items():
            with self.subTest(attr=attr, typ=typ):
                self.assertIn(attr, inst.__dict__)
                self.assertIs(type(inst.__dict__[attr]), typ)
        self.assertEqual(inst.name, "Holbertonland")
        self.assertEqual(inst.state_id, state_id)
        self.assertTrue(tic <= inst.created_at <= toc)
        self.assertEqual(inst.created_at, inst.updated_at)

    def test_name_attr(self):
        """Test that City has attribute name, and it's an empty string"""
        city = City()
        self.assertTrue(hasattr(city, "name"))
        if models.storage_t == 'db':
            self.assertEqual(city.name, None)
        else:
            self.assertEqual(city.name, "")

    @unittest.skipIf(models.storage_t != 'db1', "no test db Storage")
    def test_places_relationship(self):
        """Test cities places relationship"""
        self.cur = TestCity.db_conn.cursor()
        self.cur.execute(
            '''DROP TABLE IF EXISTS
            place_amenity, amenities, states,
            users, cities, places, reviews;
            ''')
        models.storage.reload()
        self.cur.execute('''INSERT INTO
        states (name, id)
        VALUES ("Khartoum", "123456789efef");
        ''')
        TestCity.db_conn.close()
        city = City()
        city.name = "Khartoum2"
        city.state_id = "123456789efef"
        city.save()
        models.storage.close()
        TestCity.db_conn = MySQLdb.connect(
                user=TestCity.HBNB_MYSQL_USER,
                password=TestCity.HBNB_MYSQL_PWD,
                host=TestCity.HBNB_MYSQL_HOST,
                database=TestCity.HBNB_MYSQL_DB)
        self.cur = TestCity.db_conn.cursor()
        self.cur.execute('''INSERT INTO
        users (email, password, first_name, last_name, id)
        VALUES ("janedoe@mail.com", "janedoe", "Jane", "Doe", "123456789abcd");
        ''')
        self.cur.execute(f'''INSERT INTO
        places (city_id, user_id, name,
        number_rooms, number_bathrooms,
        max_guest, price_by_night, id)
        VALUES
        ("{city.id}", "123456789abcd", "TINY PLACE",
        2, 1, 2, 79, "123456789fefe"),
        ("{city.id}", "123456789abcd", "LARG HUP",
        4, 2, 4, 89, "123456789cdcd"),
        ("{city.id}", "123456789abcd", "SUMMERRR",
        1, 1, 1, 49, "123456789abab")
        ''')
        TestCity.db_conn.close()
        places = city.places
        print(places)

    def test_state_id_attr(self):
        """Test that City has attribute state_id, and it's an empty string"""
        city = City()
        self.assertTrue(hasattr(city, "state_id"))
        if models.storage_t == 'db':
            self.assertEqual(city.state_id, None)
        else:
            self.assertEqual(city.state_id, "")

    def test_to_dict_creates_dict(self):
        """test to_dict method creates a dictionary with proper attrs"""
        c = City()
        new_d = c.to_dict()
        self.assertEqual(type(new_d), dict)
        self.assertFalse("_sa_instance_state" in new_d)
        for attr in c.__dict__:
            if attr != "_sa_instance_state":
                self.assertTrue(attr in new_d)
        self.assertTrue("__class__" in new_d)

    def test_to_dict_values(self):
        """test that values in dict returned from to_dict are correct"""
        t_format = "%Y-%m-%dT%H:%M:%S.%f"
        c = City()
        new_d = c.to_dict()
        self.assertEqual(new_d["__class__"], "City")
        self.assertEqual(type(new_d["created_at"]), str)
        self.assertEqual(type(new_d["updated_at"]), str)
        self.assertEqual(new_d["created_at"], c.created_at.strftime(t_format))
        self.assertEqual(new_d["updated_at"], c.updated_at.strftime(t_format))

    def test_str(self):
        """test that the str method has the correct output"""
        city = City()
        string = "[City] ({}) {}".format(city.id, city.__dict__)
        self.assertEqual(string, str(city))
