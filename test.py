#!/usr/bin/python3
from sqlalchemy import Column, String, Integer
import hashlib

class Test:
    m = hashlib.md5()
    def __init__(self, uid, username, password):
        usr_byte = str.encode(password)
        self.m.update(usr_byte)
        password = self.m.digest()
        self.uid = uid
        self.username = username
        self.password = password

    def __str__(self):
        return "id-{}  user-{} pass-{}".format(self.uid, self.username, self.password)
