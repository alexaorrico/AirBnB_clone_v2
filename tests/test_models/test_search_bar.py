#!/usr/bin/env python

def test_search_bar():
    homepage = '<body><header><form><input type="text" name="search" placeholder="Search"></form></header></body>'
    assert '<input type="text" name="search"' in homepage

if name == '__main__':
    test_search_bar()
