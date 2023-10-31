#!/usr/bin/python3
""" """
from time import sleep
from tests.test_models.test_base_model import test_basemodel
from models.state import State
import env
import unittest
from models.city import City


class test_state(test_basemodel):
    """ """

    def __init__(self, *args, **kwargs):
        """ """
        super().__init__(*args, **kwargs)
        self.name = "State"
        self.value = State

    def test_name3(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.name), type(None))


@unittest.skipIf(not env.DBTYPE, "not testing file storage")
class test_State_db(unittest.TestCase):
    """
    Test the State class with DBStorage
    """
    session = None

    def setUp(self) -> None:
        from models import storage
        self.session = storage.get_session()
        self.session.query(State).delete()
        self.session.commit()

    def tearDown(self) -> None:
        self.session.query(State).delete()
        self.session.commit()

    def test_save(self):
        """
        Test save method
        """
        before = self.session.query(State).count()
        new_state = State(name="California")
        new_state.save()
        states = self.session.query(State).all()
        self.assertIsInstance(states[0], State)
        self.assertEqual(states[0].name, "California")
        self.assertEqual(before + 1, len(states))

    def test_get_cities(self):
        """
        Test cities property
        """
        new_state = State(name="California")
        new_state.save()

        with self.subTest("Test with no cities"):
            cities = new_state.cities
            self.assertIsInstance(cities, list)
            self.assertEqual(len(cities), 0)

        with self.subTest("Test with one city"):
            new_city = City(name="San Francisco")
            new_state.cities.append(new_city)
            new_state.save()
            cities = new_state.cities
            self.assertIsInstance(cities, list)
            self.assertEqual(len(cities), 1)
            self.assertIsInstance(cities[0], City)
            self.assertEqual(cities[0].name, "San Francisco")
            self.assertEqual(cities[0].state_id, new_state.id)

        with self.subTest("Test with two cities"):
            new_city = City(name="Los Angeles", state_id=new_state.id)
            new_state.cities.append(new_city)
            new_state.save()
            cities = new_state.cities
            self.assertIsInstance(cities, list)
            self.assertEqual(len(cities), 2)
            self.assertIsInstance(cities[0], City)
            names = [city.name for city in cities]
            self.assertTrue("San Francisco" in names)
            self.assertTrue("Los Angeles" in names)
            self.assertEqual(cities[0].state_id, new_state.id)
            self.assertIsInstance(cities[1], City)
            self.assertEqual(cities[1].state_id, new_state.id)
