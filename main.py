from models import storage
from models.user import User
user = User(email="john@snow.com", password="johnpwd")
user.save()
storage.save()