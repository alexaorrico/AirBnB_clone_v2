#!/usr/bin/python3
"""
Command interpreter for Holberton AirBnB project
"""
import cmd
from models import storage, CNC


class HBNBCommand(cmd.Cmd):
    """
    Command inerpreter class
    """
    prompt = '(hbnb) '
    ERR = [
        '** class name missing **',
        '** class doesn\'t exist **',
        '** instance id missing **',
        '** no instance found **',
        '** attribute name missing **',
        '** value missing **',
        ]

    def preloop(self):
        """
        handles intro to command interpreter
        """
        print('.----------------------------.')
        print('|    Welcome to hbnb CLI!    |')
        print('|   for help, input \'help\'   |')
        print('|   for quit, input \'quit\'   |')
        print('.----------------------------.')

    def postloop(self):
        """
        handles exit to command interpreter
        """
        print('.----------------------------.')
        print('|  Well, that sure was fun!  |')
        print('.----------------------------.')

    def default(self, line):
        """
        default response for unknown commands
        """
        print("This \"{}\" is invalid, run \"help\" "
              "for more explanations".format(line))

    def emptyline(self):
        """
        Called when an empty line is entered in response to the prompt.
        """
        pass

    def __class_err(self, arg):
        """
        private: checks for missing class or unknown class
        """
        error = 0
        if len(arg) == 0:
            print(HBNBCommand.ERR[0])
            error = 1
        else:
            if isinstance(arg, list):
                arg = arg[0]
            if arg not in CNC.keys():
                print(HBNBCommand.ERR[1])
                error = 1
        return error

    def __id_err(self, arg):
        """
        private checks for missing ID or unknown ID
        """
        error = 0
        if (len(arg) < 2):
            error += 1
            print(HBNBCommand.ERR[2])
        if not error:
            storage_objs = storage.all()
            for key, value in storage_objs.items():
                temp_id = key.split('.')[1]
                if temp_id == arg[1] and arg[0] in key:
                    return error
            error += 1
            print(HBNBCommand.ERR[3])
        return error

    def do_airbnb(self, arg):
        """airbnb: airbnb
        SYNOPSIS: Command changes prompt string"""
        print("                      __ ___                        ")
        print("    _     _  _ _||\ |/  \ | _  _  _|_|_     _  _ _| ")
        print("|_||_)\)/(_|| (_|| \|\__/ || )(_)| |_| )\)/(_|| (_| ")
        print("   |                                                ")
        if HBNBCommand.prompt == '(hbnb) ':
            HBNBCommand.prompt = " /_ /_ _  /_\n/ //_// //_/ "
        else:
            HBNBCommand.prompt = '(hbnb) '
        arg = arg.split()
        error = self.__class_err(arg)

    def do_quit(self, line):
        """quit: quit
        USAGE: Command to quit the program
        """
        return True

    def do_EOF(self, line):
        """function to handle EOF"""
        print()
        return True

    def __isfloat(self, val):
        """
        checks if a string may be converted to a float
        """
        try:
            float(val)
            return True
        except:
            return False

    def __update_val(self, v):
        """updates string to proper type, either int, float, or
        string with proper spaces and " symbols"""
        if v[0] == '"' and v[-1] == '"':
            v = v[1:-1]
            v = v.replace('"', '\"')
            v = v.replace('_', ' ')
            return v
        if v.isdigit():
            v = int(v)
        elif self.__isfloat(v):
            v = float(v)
        return v

    def __create_dict(self, attr_dict, arg):
        """creates dictionary from input paramaters of create() function"""
        for params in arg:
            if '=' in params:
                i = params.index('=')
                if i < len(params) - 1:
                    k = params[:i]
                    v = params[(i + 1):]
                    v = self.__update_val(v)
                    attr_dict[k] = v
        return attr_dict

    def do_create(self, arg):
        """create: create [ARG] [PARAM 1] [PARAM 2] ...
        ARG = Class Name
        PARAM = <key name>=<value>
                value syntax: "<value>"
        SYNOPSIS: Creates a new instance of the Class from given input ARG
                  and PARAMS. Key in PARAM = an instance attribute.
        EXAMPLE: create City name="Chicago"
                 City.create(name="Chicago")
        """
        arg = arg.split()
        error = self.__class_err(arg)
        if error:
            return
        k = arg[0]
        class_obj = CNC[k]
        if len(arg) > 1:
            d = self.__create_dict({}, arg[1:])
        else:
            d = {}
        my_obj = class_obj(**d)
        my_obj.save()
        print(my_obj.id)

    def do_show(self, arg):
        """show: show [ARG] [ARG1]
        ARG = Class
        ARG1 = ID #
        SYNOPSIS: Prints object of given ID from given Class"""
        arg = arg.split()
        error = self.__class_err(arg)
        if not error:
            error += self.__id_err(arg)
        if not error:
            storage_objs = storage.all()
            for k, v in storage_objs.items():
                if arg[1] in k and arg[0] in k:
                    print(v)

    def do_all(self, arg):
        """all: all [ARG]
        ARG = Class
        SYNOPSIS: prints all objects of given class
        EXAMPLE: all City
                 City.all()
        """
        arg = arg.split()
        error = 0
        if arg:
            error = self.__class_err(arg)
            if error:
                return
        print('[', end='')
        l = 0
        if arg:
            storage_objs = storage.all(arg[0])
        else:
            storage_objs = storage.all()
        l = len(storage_objs)
        c = 0
        for v in storage_objs.values():
            c += 1
            print(v, end=(', ' if c < l else ''))
        print(']')

    def do_destroy(self, arg):
        """destroy: destroy [ARG] [ARG1]
        ARG = Class
        ARG1 = ID #
        SYNOPSIS: destroys object of given ID from given Class
        EXAMPLE: destroy City 1234-abcd-5678-efgh
                 City.destroy(1234-abcd-5678-efgh)
        """
        arg = arg.split()
        error = self.__class_err(arg)
        if not error:
            error += self.__id_err(arg)
        if error:
            return
        storage_objs = storage.all()
        for k in storage_objs.keys():
            if arg[1] in k and arg[0] in k:
                to_delete = storage_objs[k]
        to_delete.delete()
        storage.save()

    def __rremove(self, s, l):
        """
        private: removes characters in the input list from input string
        """
        for c in l:
            s = s.replace(c, '')
        return s

    def __check_dict(self, arg):
        """
        private: checks if the arguments input has a dictionary
        """
        if '{' and '}' in arg:
            l = arg.split('{')[1]
            l = l.split(', ')
            l = list(s.split(':') for s in l)
            d = {}
            for subl in l:
                k = subl[0].strip('"\' {}')
                v = subl[1].strip('"\' {}')
                d[k] = v
            return d
        else:
            return None

    def __handle_update_err(self, arg):
        """
        private: checks for all errors in update
        """
        d = self.__check_dict(arg)
        arg = self.__rremove(arg, [',', '"'])
        arg = arg.split()
        error = self.__class_err(arg)
        if not error:
            error += self.__id_err(arg)
        if error:
            return [0]
        valid_id = 0
        storage_objs = storage.all()
        for k in storage_objs.keys():
            if arg[1] in k and arg[0] in k:
                key = k
        if len(arg) < 3:
            print(HBNBCommand.ERR[4])
        elif len(arg) < 4:
            print(HBNBCommand.ERR[5])
        else:
            return [1, arg, d, storage_objs, key]
        return [0]

    def do_update(self, arg):
        """update: update [ARG] [ARG1] [ARG2] [ARG3]
        ARG = Class
        ARG1 = ID #
        ARG2 = attribute name
        ARG3 = value of new attribute
        SYNOPSIS: updates or adds a new attribute and value of given Class
        EXAMPLE: update City 1234-abcd-5678-efgh name Chicago
                 City.update(1234-abcd-5678-efgh, name, Chicago)
                 City.update(1234-abcd, {'name': 'Chicago', 'address': 'None'})
        """
        arg_inv = self.__handle_update_err(arg)
        if arg_inv[0]:
            arg = arg_inv[1]
            d = arg_inv[2]
            storage_objs = arg_inv[3]
            key = arg_inv[4]
            if not d:
                avalue = arg[3].strip('"')
                if avalue.isdigit():
                    avalue = int(avalue)
                storage_objs[key].bm_update({arg[2]: avalue})
            else:
                for k, v in d.items():
                    if v.isdigit():
                        v = int(v)
                    storage_objs[key].bm_update({k: v})

    def do_BaseModel(self, arg):
        """class method with .function() syntax
        Usage: BaseModel.<command>(<id>)"""
        self.__parse_exec('BaseModel', arg)

    def do_Amenity(self, arg):
        """class method with .function() syntax
        Usage: Amenity.<command>(<id>)"""
        self.__parse_exec('Amenity', arg)

    def do_City(self, arg):
        """class method with .function() syntax
        Usage: City.<command>(<id>)"""
        self.__parse_exec('City', arg)

    def do_Place(self, arg):
        """class method with .function() syntax
        Usage: Place.<command>(<id>)"""
        self.__parse_exec('Place', arg)

    def do_Review(self, arg):
        """class method with .function() syntax
        Usage: Review.<command>(<id>)"""
        self.__parse_exec('Review', arg)

    def do_State(self, arg):
        """class method with .function() syntax
        Usage: State.<command>(<id>)"""
        self.__parse_exec('State', arg)

    def do_User(self, arg):
        """class method with .function() syntax
        Usage: User.<command>(<id>)"""
        self.__parse_exec('User', arg)

    def __count(self, arg):
        """counts the number objects in File Storage"""
        args = arg.split()
        storage_objs = storage.all()
        count = 0
        for k in storage_objs.keys():
            if args[0] in k:
                count += 1
        print(count)

    def __parse_exec(self, c, arg):
        """
        private: parses the input from .function() syntax, calls matched func
        """
        CMD_MATCH = {
            '.all': self.do_all,
            '.count': self.__count,
            '.show': self.do_show,
            '.destroy': self.do_destroy,
            '.update': self.do_update,
            '.create': self.do_create,
        }
        if '(' and ')' in arg:
            check = arg.split('(')
            new_arg = "{} {}".format(c, check[1][:-1])
            for k, v in CMD_MATCH.items():
                if k == check[0]:
                    if ((',' or '"' in new_arg) and k != '.update'):
                        new_arg = self.__rremove(new_arg, ['"', ','])
                    v(new_arg)
                    return
        self.default(arg)

if __name__ == '__main__':
    """
    MAIN Loop
    """
    HBNBCommand().cmdloop()
