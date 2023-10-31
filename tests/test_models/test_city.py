#!/usr/bin/python3
""" """
from tests.test_models.test_base_model import test_basemodel
from models.city import City
from models.state import State
import env
import unittest


class test_City(test_basemodel):
    """ """

    def __init__(self, *args, **kwargs):
        """ """
        super().__init__(*args, **kwargs)
        self.name = "City"
        self.value = City

    def test_state_id(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.state_id), type(None))

    def test_name(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.name), type(None))


@unittest.skipIf(not env.DBTYPE, "not testing file storage")
class test_City_db(unittest.TestCase):
    """
    Test the City class with DBStorage
    """
    session = None

    def setUp(self) -> None:
        from models import storage
        self.session = storage.get_session()
        self.session.query(City).delete()
        self.session.commit()

    def tearDown(self) -> None:
        self.session.query(City).delete()
        self.session.commit()

    def test_save(self):
        """
        Test save method
        """
        before = self.session.query(City).count()
        new_state = State(name="California")
        new_state.save()
        new_city = City(name="San Francisco", state_id=new_state.id)
        new_city.save()
        qcities = self.session.query(City)
        self.assertEqual(before + 1, qcities.count())
        cities = qcities.all()
        self.assertIsInstance(cities[0], City)
        self.assertEqual(cities[0].name, "San Francisco")
        self.assertEqual(cities[0].state_id, new_state.id)
