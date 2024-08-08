<center><h1>HBNB Web Flask</h1></center>
11;rgb:0000/0000/0000
This repository is a continuation of the already existing HBNB project. This stage of the project implements a Flask application that provides an easy way to define the route of our web application. The Jinja2 template which is readily availabe in Flask allows the application to generate dynamic contents. In the previous project, a data storage was implemented. This project the data stored is queried, filtered and used within our templates. When a valid route is accessed the page generated can be displayed back to the user that made the request.

N:B GET request method is used in all the application routes.

---

<center><h3>Repository Contents by Project Task</h3> </center>

|Tasks | Files | Description |
| ------ | ----- | ----- |
| 0. route: / | 0-hello_route.py | display "Hello HBNB!"
| 1. route: /hbnb | 1-hbnb_route.py | display "HBNB"
| 2. route: /c/<text> | 2.c_route.py | display "C" followed by the value of the text variable(replacing undersore _ symbols with a space)
