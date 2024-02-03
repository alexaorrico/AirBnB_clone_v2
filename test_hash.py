#!/usr/bin/python3


from models.user import User
from models import storage

new_user = User(email="Abdou20@gmail.com", password="Abdelwadoud14")
user_id = new_user.id
storage.new(new_user)
storage.save()
user = storage.get(User, user_id)
print(user.to_dict())
