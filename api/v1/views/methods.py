#!/usr/bin/python3
from flask import jsonify
from models import storage
from models.state import State
from flask import abort, request, make_response


class ApiMethod:
    def get_objects(self, cls):
        objs = storage.all(cls)
        mylist = []

        for key, value in objs.items():
            mylist.append(value.to_dict())

        return mylist

    def get_one_object(self, cls, obj_id):
        obj = storage.get(cls, obj_id)
        if not obj:
            return None
        else:
            return obj.to_dict()

    def delete_one_object(self, cls, obj_id):
        obj = storage.get(cls, obj_id)
        if not obj:
            return False
        else:
            storage.delete(obj)
            storage.save()
            return True

    def create_object(self, cls, **kwargs):
        obj = cls(**kwargs)
        obj.save()
        return obj.to_dict()

    def update_objects(self, cls, obj_id, **kwargs):
        obj = storage.get(cls, obj_id)
        if obj:

            for key, value in kwargs.items():
                setattr(obj, key, value)

                storage.save()

                return obj.to_dict()
        else:
            return None
