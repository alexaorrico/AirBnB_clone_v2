#!/usr/bin/python3
"""Testing Documentation of a module"""

from importlib import import_module
import sys

if len(sys.argv) != 2:
    print("Usage: python3 script_name.py module_name")
else:
    module_name = sys.argv[1]

    try:
        m_imported = import_module(module_name)
        if m_imported.__doc__:
            print(m_imported.__doc__)
        else:
            print(module_name + " has no documentation.")
            print("Module has no documentation.")
    except ImportError as e:
        print(e)
        print("Module not found or cannot be imported.")
