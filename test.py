#!/usr/bin/python3
from importlib import import_module
import sys

m_imported = import_module(sys.argv[1])
if m_imported.__doc__ is None:
    print('No module documentation')
else:
    print('Ok')
