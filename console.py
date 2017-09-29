#!/usr/bin/python3
""" console """

import cmd
import models
from models.base_model import BaseModel


class HBNBCommand(cmd.Cmd):
    """ HBNH console """
    prompt = '(hbnb) '

    def do_EOF(self, arg):
        """Exits console"""
        return True

    def emptyline(self):
        """ overwriting the emptyline method """
        return False

    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True

    def do_create(self, arg):
        """Creates a new instance of a class"""
        classes = ["BaseModel"]
        args = arg.split()
        if len(args) == 0:
            print("** class name missing **")
            return False
        if args[0] in classes:
            instance = eval(args[0])()
        else:
            print("** class doesn't exist **")
            return False
        print(instance.id)

if __name__ == '__main__':
    HBNBCommand().cmdloop()
