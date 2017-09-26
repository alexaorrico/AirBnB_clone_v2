#!/usr/bin/python3
""" console """

import cmd
import models

class HBNBCommand(cmd.Cmd):
    """ HBNH console """
    prompt = '(hbnb)'

    def do_EOF(self, arg):
        """Exits console"""
        return True

    def emptyline(self):
        """ overwriting the emptyline method """
        pass

    def do_quit( self, arg):
        """Quit command to exit the program"""
        return True

#    def do_create(self, arg):


if __name__ == '__main__':
    HBNBCommand().cmdloop()
