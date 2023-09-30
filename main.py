from models import storage

all_obj = storage.all()

for key in all_obj.keys():
    obj = all_obj[key]
    print(obj.to_dict())
