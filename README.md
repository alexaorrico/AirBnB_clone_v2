#Synopsis
"I am working on an Airbnb clone project, where I am creating a copy of Airbnb. I am currently in the process of implementing specific features, which I will outline below as they are completed. In this stage, I am integrating an additional storage option. Depending on the chosen database system (file storage or database storage), I use JSON or MySQL and SQLalchemy through Python. For application deployment, I employ Fabric.

#Key Features:
Command Interpreter
Description:
The Command Interpreter is my primary tool for managing the entire application's functionality directly from the command line. With it, I can:

#Create new objects.
Retrieve objects from various sources, including files and databases.
Execute operations on objects, such as counting and statistical computations.
Update object attributes.
Delete objects."

#Usage
To launch the console application in interactive mode simply run:

console.py 

or to use the non-interactive mode run:

echo "your-command-goes-here" | ./console.py 

#Commands
Commands	Description	Usage
help or ?	Displays the documented commands.	help
quit	Exits the program.	quit
EOF	Ends the program. Used when files are passed into the program.	N/A
create	Creates a new instance of the <class_name>. Creates a Json file with the object representation. and prints the id of created object.	create <class_name>
show	Prints the string representation of an instance based on the class name and id.	show <class_name class_id>
destroy	Deletes and instance base on the class name and id.	destroy <class_name class_id>
all	Prints all string representation of all instances based or not on the class name	all or all <class_name class_id>
update	Updates an instance based on the class name and id by adding or updating attribute	update <class_name class_id key value>
Resources
Fabric: Usage1, Usage2, Documenation
Nginx: Beginner's Config file, Root vs Alias,
#Tests
If you wish to run at the test for this application all of the test are located under the test/ folder and can execute all of them by simply running:

python3 -m unittest discover tests 

from the root directory.

#Bugs
No known bugs at this time.
