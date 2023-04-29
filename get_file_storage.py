#!/usr/bin/python3

def test_db_storage_get():
    db = DBStorage()
    obj = MyModel(name='foo')
    db.add(obj)
    db.commit()
    result = db.get(MyModel, obj.id)
    assert result == obj
