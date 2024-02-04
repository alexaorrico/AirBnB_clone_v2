import unittest

# Configure the unittest output
unittest.runner._WritelnDecorator.stream = open("/dev/null", "w")
