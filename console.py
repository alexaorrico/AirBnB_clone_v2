#!/usr/bin/python3
"""
Defines a program `console` that contains the entry point of the command
interpreter.
Requirements:
  - You must use the module cmd
  - Your class definition must be: class HBNBCommand(cmd.Cmd):
  - Your command interpreter should implement:
  - quit and EOF to exit the program
  - help (this action is provided by default by cmd but you should keep it
    updated and documented as you work through tasks) a custom prompt: (hbnb)
  - an empty line + ENTER shouldn’t execute anything
  - Your code should not be executed when imported
"""
import cmd
import sys
from models import storage
from models.user import User
from models.city import City
from models.place import Place
from models.state import State
from models.review import Review
from models.amenity import Amenity
from models.base_model import BaseModel

# define global class dict
cls_dict = {"BaseModel": BaseModel, "User": User, "State": State,
            "City": City, "Amenity": Amenity, "Place": Place, "Review": Review}


class HBNBCommand(cmd.Cmd):
    """
    Defines the command interpreter
    """

    prompt = '(hbnb) '

    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True

    def do_EOF(self, arg):
        """EOF command to exit the program"""
        return True

    def emptyline(self):
        """Do nothing when an empty line is entered"""
        pass

    def do_create(self, arg):
        """
        Creates a new instance of BaseModel, save it (to JSON file)
        and prints the id
        """
        # get class name
        cls = cls_dict.get(arg)

        # validate input
        if not arg:
            print("** class name missing **")
        elif cls is None:
            print("** class doesn't exist **")
        else:
            obj = cls()  # create instance
            storage.new(obj)
            storage.save()
            print(obj.id)

    def do_show(self, line):
        """
        Prints the string representation of an instance based on the
        class name and id
        """
        args = line.split()
        if len(args) != 0:
            if len(args) == 2:
                cls = cls_dict.get(args[0])
                if cls:
                    objs = storage.all()
                    # create key
                    obj_key = "{}.{}".format(args[0], args[1])
                    if obj_key in objs:
                        obj = objs.get(obj_key)
                        print(str(obj))
                    else:
                        print("** no instance found **")
                else:
                    print("** class doesn't exist **")
            else:
                print("** instance id missing **")
        else:
            print("** class name missing **")

    def do_destroy(self, line):
        """
        Deletes an instance based on the class name and id (save the change
        into the JSON file)
        """
        args = line.split()
        if len(args) != 0:
            if len(args) == 2:
                cls = cls_dict.get(args[0])
                if cls:
                    objs = storage.all()
                    obj_key = "{}.{}".format(args[0], args[1])
                    if obj_key in objs:
                        del objs[obj_key]
                        storage.save()
                    else:
                        print("** no instance found **")
                else:
                    print("** class doesn't exist **")
            else:
                print("** instance id missing **")
        else:
            print("** class name missing **")

    def do_all(self, arg):
        """
        Prints all string representation of all instances based or not on
        the class name
        """
        objs = storage.all()
        objs_list = []
        if arg:
            # print object of the class provided
            cls = cls_dict.get(arg)
            if cls:
                for key, obj in objs.items():
                    cls_name = key.split('.')[0]
                    if arg == cls_name:
                        objs_list.append(str(obj))
                print(objs_list)
            else:
                print("** class doesn't exist **")
        else:
            # print all objects
            for obj in objs.values():
                objs_list.append(str(obj))
            print(objs_list)

    def do_update(self, line):
        """
        Updates an instance based on the class name and id by adding or
        updating attribute (save the change into the JSON file
        """
        args = line.split()
        if len(args) >= 4:
            cls = cls_dict.get(args[0])
            if cls:
                objs = storage.all()
                obj_key = "{}.{}".format(args[0], args[1])
                if obj_key in objs:
                    obj = objs.get(obj_key)

                    # convert attribute_value to correct data type
                    try:
                        value = float(args[3])
                        if value.is_integer():
                            attr_value = int(value)
                        else:
                            attr_value = value
                    except ValueError:
                        # remove quotes
                        value = args[3].strip('\'"')
                        attr_value = str(value)

                    # update object
                    setattr(obj, args[2], attr_value)

                    # save update to file
                    storage.save()
                else:
                    print("** no instance found **")
            else:
                print("** class doesn't exist **")
        else:
            if len(args) == 0:
                print("** class name missing **")
            if len(args) == 1:
                print("** instance id missing **")
            if len(args) == 2:
                print("** attribute name missing **")
            if len(args) == 3:
                print("** value missing **")

    def default(self, line):
        """executes command methods not defined"""

        # list of commands
        cmd_list = ["all", "count", "show", "destroy", "update"]

        # extract command name ,class name
        args = line.split('.')
        cls_name = args[0]
        cmd = args[1].split('(')
        cmd_name = cmd[0]

        # extract function arguments
        args_list = cmd[1].split(',')
        if len(args_list) > 0:
            id = args_list[0].strip("\"'")
            # string to pass to function
            cmd_string = "{} {}".format(cls_name, id)

        if len(args_list) > 2:
            attr_name = args_list[1].strip("\"'")
            attr_value = args_list[2].strip("\"'")
            # string to pass to function
            cmd_string = "{} {} {} {}".format(cls_name, id,
                                              attr_name, attr_value)

        cls = cls_dict.get(cls_name)
        if cls:
            if cmd_name in cmd_list:
                if cmd_name == "all":
                    # execute <class name>.all() command
                    self.do_all(cls_name)

                elif cmd_name == "count":
                    # execute <class name>.count() command
                    objs = storage.all()
                    cls_objs_dict = {}
                    for key, obj in objs.items():
                        name = key.split('.')[0]
                        if name == cls_name:
                            cls_objs_dict[key] = obj
                    # print count
                    print(len(cls_objs_dict))

                elif cmd_name == "show":
                    # execute <class name>.show(<id>) command
                    print(cmd_string)
                    self.do_show(cmd_string)

                elif cmd_name == "destroy":
                    # execute <class name>.destroy(<id>) command
                    self.do_destroy(cmd_string)

                elif cmd_name == "update":
                    # execute <class name>.update(<id>, <attribute name>,
                    # <attribute value>)
                    print(cmd_string)
                    self.do_update(cmd_string)


if __name__ == '__main__':
    HBNBCommand().cmdloop()
