#!/usr/bin/python3
"""Unit test of the requirements for the project in general"""

import unittest
import os


class Test_Project(unittest.TestCase):
    """Class to test the project"""

    def test_project(self):
        """Check the project requirements:
        - existence of all files and directories in the correct location
        - all the python scripts are executable
        - all the files end in a new line
        - all the files start with a #!/usr/bin/python
        - all the files are written with the pycodestyle standard
        - there is a readme
        - all the modules are documented
        """

        # PEP8
        pep8 = "pep8 --count ."
        self.assertEqual(os.system(pep8), 0)

        # Readme file
        self.assertTrue(os.path.isfile('README.md'))

        # Package
        self.assertTrue(os.path.isfile('./models/__init__.py'))
        self.assertTrue(os.path.isfile('./models/engine/__init__.py'))
        self.assertTrue(os.path.isfile('./tests/__init__.py'))
        self.assertTrue(os.path.isfile('./tests/test_models/__init__.py'))
        self.assertTrue(os.path.isfile(
            './tests/test_models/test_engine/__init__.py'))

        flist = ['console.py', './models/base_model.py',
                 './models/city.py', './models/place.py',
                 './models/review.py', './models/state.py',
                 './models/user.py',
                 './models/engine/file_storage.py']

        for filee in flist:
            # existence of all files and directories in the correct location
            self.assertTrue(os.path.isfile(filee), filee)

            # files are executable
            self.assertTrue(os.access(filee, os.X_OK), filee)

            # First and last line
            with open(filee) as f:
                first = f.readline()
                last = f.read()[-1]
                self.assertTrue(first == '#!/usr/bin/python3\n', filee)
                self.assertTrue(last == '\n', filee)

            # documentation of module
            self.assertTrue(len(filee.__doc__) > 5)


if __name__ == '__main__':
    unittest.main()
