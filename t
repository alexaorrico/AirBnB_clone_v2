#!/usr/bin/python3

from models.user import User
user_data = {
    "email": "example@example.com",
    "password": "secure_password",
    "first_name": "John",
    "last_name": "Doe"
}

user = User(**user_data)
print(f"Original Password: {user_data['password']}")
print(f"Hashed Password: {user.password}")

# Test to_dict() Method
user_dict = user.to_dict()
print("to_dict() Result:")
print(user_dict)

# Test to_dict(save_to_disk=True) Method
user_dict_disk = user.to_dict(save_to_disk=True)
print("to_dict(save_to_disk=True) Result:")
print(user_dict_disk)
