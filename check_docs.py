#!/usr/bin/python3
"""Testing documentation of a module"""
from importlib import import_module
import sys

# try:
#     mod_to_check = import_module(sys.argv[1])
#     if mod_to_check.__doc__ is None:
#         print("No module documentation!")
#     else:
#         print("Docstring: {}".format(mod_to_check.__doc__))
# except Exception as e:
#     print(e)
m_imported = import_module(sys.argv[1])

if m_imported.__doc__ is None:
    print("No module documentation", end="")
else:
    print("OK", end="")
