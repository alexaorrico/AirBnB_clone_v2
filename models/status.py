#!/usr/bin/python3
"""status model for json responses
"""
class Status():
    """status class for json responses"""
    def __init__(self, status="OK"):
        """init status class, defaults to OK"""
        self.status = status
