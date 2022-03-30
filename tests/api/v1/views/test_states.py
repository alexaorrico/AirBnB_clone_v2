#!/usr/bin/python3
"""
Contains the TestStateDocs classes
"""

from datetime import datetime
import inspect
import models
from models import state
from models.base_model import BaseModel
import unittest
State = state.State
import api.v1.views.states


class TestStates(unittest.TestCase):
    '''
    Test the states modules
    '''
    def test_all_states(self):
        '''
        test state route
        '''
        all_states = api.v1.views.states()
        self.assertTrue(all_states)


if __name__ == "__main__":
    unittest.main
