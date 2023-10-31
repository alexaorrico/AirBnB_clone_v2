#!/usr/bin/python3
""" Module for testing db storage"""
import datetime
import unittest

import MySQLdb

import env
from models import storage
from models.user import User


def clear_db(conn):
    from models.engine.db_storage import classes
    cursor = conn.cursor()
    for table in classes:
        tablename = classes[table].__tablename__
        cursor.execute("DELETE FROM {}".format(tablename))
    conn.commit()


@unittest.skipIf(env.HBNB_TYPE_STORAGE != 'db', "not testing file storage")
class test_DbStorage(unittest.TestCase):
    """ Class to test the db storage method """
    cursor = None
    db = None

    data = {
        "first_name": "test",
        "last_name": "doe",
        "email": "test@gmail.com",
        "password": "test"
    }

    def setUp(self):
        """ Set up test environment """
        self.db = MySQLdb.connect(
            host=env.HBNB_MYSQL_HOST,
            user=env.HBNB_MYSQL_USER,
            passwd=env.HBNB_MYSQL_PWD,
            db=env.HBNB_MYSQL_DB
        )
        self.cursor = self.db.cursor()
        clear_db(self.db)

    def tearDown(self):
        self.cursor.close()
        self.db.close()

    def test_created_engine(self):
        """ Confirm engine is created """
        self.assertIsNotNone(storage._DBStorage__engine)

    def test_created_session(self):
        """ Confirm session is created """
        self.assertIsNotNone(storage._DBStorage__session)

    def test_obj_list_empty(self):
        """ __objects is initially empty """
        self.assertEqual(len(storage.all()), 0)

    def test_all(self):
        """ __objects is properly returned """
        temp = storage.all()
        self.assertIsInstance(temp, dict)

    def test_new(self):
        """ New User is correctly added """
        new = User(**self.data)
        new.updated_at = datetime.datetime.now()
        storage.new(new)
        self.cursor.execute("SELECT * FROM users")
        all_objs = self.cursor.fetchall()
        self.assertEqual(len(all_objs), 0)
        storage.save()

    def test_save(self):
        """ DbStorage save method """
        new = User(**self.data)
        new.updated_at = datetime.datetime.now()
        storage.new(new)
        storage.save()
        self.cursor.execute("SELECT first_name FROM users")
        all_objs = self.cursor.fetchall()
        self.assertEqual(len(all_objs), 1)
        self.assertEqual(all_objs[0][0], self.data['first_name'])

    def test_key_format(self):
        """ Key is properly formatted """
        new = User(**self.data)
        new.updated_at = datetime.datetime.now()
        storage.new(new)
        storage.save()
        _id = new.to_dict()['id']
        objs = storage.all(User)
        for key in objs.keys():
            temp = key
            self.assertEqual(temp, 'User' + '.' + _id)

    def test_all_key_format(self):
        """
        Key is properly formatted when calling all
        without passing a class
        """
        new = User(**self.data)
        new.updated_at = datetime.datetime.now()
        storage.new(new)
        storage.save()
        _id = new.to_dict()['id']
        keys = storage.all().keys()
        expected = 'User' + '.' + _id
        self.assertIn(expected, keys)

    def test_storage_var_created(self):
        """ DbStorage object storage created """
        from models.engine.db_storage import DBStorage
        self.assertEqual(type(storage), DBStorage)
