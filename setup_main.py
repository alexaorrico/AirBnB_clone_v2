#!/usr/bin/python3
import inspect
import io
import sys
import cmd
import shutil
import os

"""
 Backup console file
"""
if os.path.exists("tmp_console_main.py"):
    shutil.copy("tmp_console_main.py", "console.py")
shutil.copy("console.py", "tmp_console_main.py")


"""
 Updating console to remove "__main__"
"""
with open("tmp_console_main.py", "r") as file_i:
    console_lines = file_i.readlines()
    with open("console.py", "w") as file_o:
        in_main = False
        for line in console_lines:
            if "__main__" in line:
                in_main = True
            elif in_main:
                if "cmdloop" not in line:
                    file_o.write(line.lstrip("    ")) 
            else:
                file_o.write(line)

import console


"""
 Create console
"""
console_obj = "HBNBCommand"
for name, obj in inspect.getmembers(console):
    if inspect.isclass(obj) and issubclass(obj, cmd.Cmd):
        console_obj = obj

my_console = console_obj(stdout=io.StringIO(), stdin=io.StringIO())
my_console.use_rawinput = False


"""
 Exec command
"""
def exec_command(my_console, the_command, last_lines = 1):
    my_console.stdout = io.StringIO()
    real_stdout = sys.stdout
    sys.stdout = my_console.stdout
    my_console.onecmd(the_command)
    sys.stdout = real_stdout
    lines = my_console.stdout.getvalue().split("\n")
    return "\n".join(lines[(-1*(last_lines+1)):-1])


"""
 Tests
"""
# Amenities
amenity_id_0 = exec_command(my_console, "create Amenity name=\"Wifi\"")
if amenity_id_0 is None or amenity_id_0 == "":
    print("FAIL: Can't create Amenity")
amenity_id_1 = exec_command(my_console, "create Amenity name=\"Ethernet\"")
if amenity_id_1 is None or amenity_id_1 == "":
    print("FAIL: Can't create Amenity")
amenity_id_2 = exec_command(my_console, "create Amenity name=\"Soap\"")
if amenity_id_2 is None or amenity_id_2 == "":
    print("FAIL: Can't create Amenity")
amenity_id_3 = exec_command(my_console, "create Amenity name=\"Bed\"")
if amenity_id_3 is None or amenity_id_3 == "":
    print("FAIL: Can't create Amenity")

print("OK", end="")

shutil.copy("tmp_console_main.py", "console.py")

