"""Defines unnittests for models/engine/db_storage.py."""
import models
import unittest
from os import getenv
from models.base_model import Base
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.engine.db_storage import DBStorage
from models.engine.file_storage import FileStorage
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.engine.base import Engine


class TestDBStorage(unittest.TestCase):
    """Unittests for testing the DBStorage class."""

    @classmethod
    def setUpClass(self):
        """DBStorage testing setup.
        """
        if type(models.storage) == DBStorage:
            self.storage = DBStorage()
            Base.metadata.create_all(self.storage._DBStorage__engine)
            Session = sessionmaker(bind=self.storage._DBStorage__engine)
            self.storage._DBStorage__session = Session()
            self.state = State(name="California")
            self.storage._DBStorage__session.add(self.state)
            self.city = City(name="San_Jose", state_id=self.state.id)
            self.storage._DBStorage__session.add(self.city)
            self.user = User(email="poppy@holberton.com", password="betty")
            self.storage._DBStorage__session.add(self.user)
            self.place = Place(city_id=self.city.id, user_id=self.user.id,
                               name="School")
            self.storage._DBStorage__session.add(self.place)
            self.amenity = Amenity(name="Wifi")
            self.storage._DBStorage__session.add(self.amenity)
            self.review = Review(place_id=self.place.id, user_id=self.user.id,
                                 text="stellar")
            self.storage._DBStorage__session.add(self.review)
            self.storage._DBStorage__session.commit()

    def test_docstrings(self):
        self.assertIsNotNone(DBStorage.__doc__)
        self.assertIsNotNone(DBStorage.all.__doc__)
        self.assertIsNotNone(DBStorage.new.__doc__)
        self.assertIsNotNone(DBStorage.save.__doc__)
        self.assertIsNotNone(DBStorage.delete.__doc__)
        self.assertIsNotNone(DBStorage.reload.__doc__)

    @unittest.skipIf(type(models.storage) == FileStorage,
                     "Testing FileStorage")
    def test_attributes(self):
        self.assertTrue(isinstance(self.storage._DBStorage__engine, Engine))
        self.assertTrue(isinstance(self.storage._DBStorage__session, Session))

    def test_methods(self):
        self.assertTrue(hasattr(DBStorage, "__init__"))
        self.assertTrue(hasattr(DBStorage, "all"))
        self.assertTrue(hasattr(DBStorage, "new"))
        self.assertTrue(hasattr(DBStorage, "save"))
        self.assertTrue(hasattr(DBStorage, "delete"))
        self.assertTrue(hasattr(DBStorage, "reload"))

    @unittest.skipIf(type(models.storage) == FileStorage,
                     "Testing FileStorage")
    def test_init(self):
        """Test initialization."""
        self.assertTrue(isinstance(self.storage, DBStorage))

    @unittest.skipIf(type(models.storage) == FileStorage,
                     "Testing FileStorage")
    def test_all(self):
        """Test default all method."""
        obj = self.storage.all()
        self.assertEqual(type(obj), dict)
        self.assertEqual(len(obj), len(self.storage.all()))

    @unittest.skipIf(type(models.storage) == FileStorage,
                     "Testing FileStorage")
    def test_new(self):
        st = State(name="Washington")
        self.storage.new(st)
        x = self.storage._DBStorage__session.query(
            State).filter(State.id == st.id).first()
        self.assertEqual(st, x)

    @unittest.skipIf(type(models.storage) == FileStorage,
                     "Testing FileStorage")
    def test_get(self):
        state = State(name='Albania')
        self.storage.new(state)
        x = self.storage.get(State, state.id)
        self.assertEqual(x, state)

    # @unittest.skipIf(models.storage == FileStorage,
    #                  'Testing Filestorage')
    # def test_count(self):
    #     state = State(name='another')
    #     state.save()
    #     self.assertEqual(len(self.storage.all()), self.storage.count())
    #     self.assertEqual(len(self.storage.all(State)),
    #                      self.storage.count(State))


if __name__ == "__main__":
    unittest.main()
