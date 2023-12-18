#!/usr/bin/python3
""" console """

import cmd
from datetime import datetime
import models
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import shlex  # for splitting the line along spaces except in double quotes

classes = {"Amenity": Amenity, "BaseModel": BaseModel, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


class HBNBCommand(cmd.Cmd):
    """ HBNH console """
    prompt = '(hbnb) '

    # Quit commands and  Emptyline
    # ============================================================ #

    def do_EOF(self, arg):
        """Exits console"""
        return True

    def emptyline(self):
        """ overwriting the emptyline method """
        return False

    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True

    def _key_value_parser(self, args):
        """creates a dictionary from a list of strings"""
        new_dict = {}
        for arg in args:
            if "=" in arg:
                kvp = arg.split('=', 1)
                key = kvp[0]
                value = kvp[1]
                if value[0] == value[-1] == '"':
                    value = shlex.split(value)[0].replace('_', ' ')
                else:
                    try:
                        value = int(value)
                    except Exception:
                        try:
                            value = float(value)
                        except Exception:
                            continue
                new_dict[key] = value
        return new_dict

    # Create
    # ============================================================ #

    def do_create(self, arg):
        """Creates a new instance of a class"""
        args = arg.split()
        if len(args) == 0:
            print("** class name missing **")
            return False
        if args[0] in classes:
            new_dict = self._key_value_parser(args[1:])
            instance = classes[args[0]](**new_dict)
        else:
            print("** class doesn't exist **")
            return False
        print(instance.id)
        instance.save()

    # Show instance
    # ============================================================ #

    def do_show(self, arg):
        """Prints an instance as a string based on the class and id"""
        args = shlex.split(arg)
        if len(args) == 0:
            print("** class name missing **")
            return False
        if args[0] in classes:
            if len(args) > 1:
                key = args[0] + "." + args[1]
                if key in models.storage.all():
                    print(models.storage.all()[key])
                else:
                    print("** no instance found **")
            else:
                print("** instance id missing **")
        else:
            print("** class doesn't exist **")

    # Destroy
    # ============================================================ #

    def do_destroy(self, line):
        """ Deletes an instance based on class name + ID """
        if not line:
            print("** class name missing **")
            return

        args = shlex.split(line)

        if len(args) < 2:
            print("** instance id missing **")
            return

        class_name = args[0]
        instance_id = args[1]

        if class_name not in models.classes:
            print("** class doesn't exist **")
            return

        all_objects = models.storage.all()
        key = "{}.{}".format(class_name, instance_id)

        if key not in all_objects:
            print("** no instance found **")
            return

        del all_objects[key]
        models.storage.save()

    # Show all instances
    # ============================================================ #

    def do_all(self, arg):
        """Prints string representations of instances"""
        args = shlex.split(arg)
        obj_list = []
        if len(args) == 0:
            obj_dict = models.storage.all()
        elif args[0] in classes:
            obj_dict = models.storage.all(classes[args[0]])
        else:
            print("** class doesn't exist **")
            return False
        for key in obj_dict:
            obj_list.append(str(obj_dict[key]))
        print("[", end="")
        print(", ".join(obj_list), end="")
        print("]")

    # Update instance
    # ============================================================ #

    def do_update(self, line):
        """Update an instance and save it"""
        if not line:
            print("** class name missing **")
            return

        args = shlex.split(line)

        class_name = args[0]

        if class_name not in models.classes:
            print("** class doesn't exist **")
            return

        if len(args) < 2:
            print("** instance id missing **")
            return

        if len(args) < 3:
            print("** attribute name missing **")
            return

        if len(args) < 4:
            print("** value missing **")
            return

        instance_id = args[1]
        key = "{}.{}".format(class_name, instance_id)
        all_objects = models.storage.all()

        if key not in all_objects:
            print("** no instance found **")
            return

        # loop step per 2
        for idx in range(2, len(args), 2):
            attribut_name = args[idx].replace("{", "").replace(":", "")
            attribut_value = args[idx + 1].replace("}", "")

            if attribut_name in models.int_attrs:
                setattr(all_objects[key], attribut_name, int(attribut_value))

            elif attribut_name in models.float_attrs:
                setattr(all_objects[key], attribut_name, float(attribut_value))

            else:
                setattr(all_objects[key], attribut_name, attribut_value)

            all_objects[key].save()

    # Count instances in json (all or per class)
    # ============================================================ #

    def do_count(self, line):
        """Count instances"""
        if not line:
            print("** class name missing **")
            return

        args = shlex.split(line)
        class_name = args[0]

        if class_name not in models.classes:
            print("** class doesn't exist **")
            return

        all_objects = models.storage.all()

        count = 0

        for key in all_objects.keys():
            name = key.split('.')[0]
            if name == class_name:
                count += 1

        print(count)

    # Alternative command syntax
    # ============================================================ #

    def precmd(self, line):
        """handle alt syntax"""
        if not line:
            return line

        if "." not in line:
            return line

        class_and_cmd = line.split("(")[0]
        class_name = class_and_cmd.split(".")[0]

        if class_name not in models.classes:
            return line

        command = class_and_cmd.split(".")[1]
        new_line = f"{command} {class_name}"

        # get all attributs inside ()
        args = line.split("(")[1].replace(")", "").split(",")

        if len(args) > 0:
            instance_id = args[0]
            new_line += f" {instance_id}"

        if len(args) > 1:
            for idx in range(1, len(args)):
                new_line += f" {args[idx]}"
            print(new_line)

        return new_line

    # Default error message
    # ============================================================ #

    def default(self, line):
        print(f"*** Unknown syntax: {line}")


if __name__ == '__main__':
    HBNBCommand().cmdloop()
