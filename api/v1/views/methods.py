#!/usr/bin/python3
"""base methods api"""

from flask import jsonify
from models import storage
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review
from flask import abort, request, make_response


class ApiMethod:
    """base methods api"""
    def get_objects(self, cls):
        """base methods api"""
        objs = storage.all(cls)
        mylist = []
        for key, value in objs.items():
            mylist.append(value.to_dict())
        return mylist

    def get_one_object(self, cls, obj_id):
        """base methods api"""
        obj = storage.get(cls, obj_id)
        if not obj:
            return None
        else:
            return obj.to_dict()

    def delete_one_object(self, cls, obj_id):
        """base methods api"""
        obj = storage.get(cls, obj_id)
        if not obj:
            return False
        else:
            storage.delete(obj)
            storage.save()
            return True

    def create_object(self, cls, **kwargs):
        """base methods api"""
        obj = cls(**kwargs)
        obj.save()
        return obj.to_dict()

    def update_objects(self, cls, obj_id, **kwargs):
        """base methods api"""
        obj = storage.get(cls, obj_id)
        if obj:
            for key, value in kwargs.items():
                setattr(obj, key, value)
            storage.save()
            return obj.to_dict()
        else:
            return None

    def get_object_byid(self, cls, obj_id):
        """ retrieve ojects associated to another Object. ej: an state
        has many cities """
        clss = {'cities': 'State', 'amenities': 'Place', 'places': 'City',
                'reviews': 'Place'}
        myobj = storage.get(cls, obj_id)
        if not myobj:
            return None
        mylist = []
        att = ''
        for k, v in clss.items():
            if cls == v:
                att = k
        for obj in getattr(myobj, att):
            mylist.append(obj.to_dict())
        return mylist
