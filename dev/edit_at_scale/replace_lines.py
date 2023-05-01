#!/usr/bin/python3
import os
oldstring = """        permissions = str(oct(file_stat[0]))
        actual = int(permissions[5:-2]) >= 5"""
newstring = """        permissions = str(oct(file_stat[0]))
        actual = int(permissions[5:-2]) >= 5"""
for dname, dirs, files in os.walk("./"):
    for fname in files:
        fpath = os.path.join(dname, fname)
        with open(fpath) as f:
            s = f.read()
        s = s.replace(oldstring, newstring)
        with open(fpath, "w") as f:
            f.write(s)
