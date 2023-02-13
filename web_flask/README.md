<h1 style="text-align: center;">
	<a href='https://intranet.alxswe.com/projects/290'>
		0x04. AirBnB clone - Web framework
	</a>
</h1>


## Resources
* [name_1](link)
* [Flask](https://flask.palletsprojects.com/en/2.2.x/quickstart/)
* [name_3](link)


## Project Overview

- [**Mandatory Task**](#mandatory-task)
	- [0. Hello Flask!](0-hello_route.py)
	- [1. HBNB](1-hbnb_route.py)
	- [2. C is fun!](2-c_route.py)
	- [3. Python is cool!](3-python_route.py)
	- [4. Is it a number?](4-number_route.py)
	- [5. Number template](5-number_template.py)
	- [6. Odd or even?](6-number_odd_or_even.py)
	- [7. Improve engines](models/engine/)
	- [8. List of states](7-states_list.py)
	- [10. States and State](9-states.py)
- [**Advanced Task**](#advanced-task)
	- [Task_013](link_to_file)
	- [Task_013](link_to_file)
	- [Task_014](link_to_file)

---



<h2 style="text-align: center;">Tasks</h2>

### Mandatory Task
#### 0. Hello Flask!

**Problem:** Write a script that starts a Flask web application:

**Requirements:**
* Your web application must be listening on `0.0.0.0`, port `5000`
* Routes:
	* `/`: display “Hello HBNB!”
* You must use the option `strict_slashes=False` in your route definition

```
AirBnB_clone_v2(master)➜ python3 -m web_flask.0-hello_route
 * Serving Flask app '0-hello_route'
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)

-------------------------------- Terminal 2 --------------------------------
imitor＠excalibur:~$ curl 0.0.0.0:5000 ; echo "" | cat -e
Hello HBNB!$
```
- [x] *File:* [0-hello_route.py](0-hello_route.py)

---

#### 1. HBNB

**Problem:** Write a script that starts a Flask web application:

**Requirements:**
* Your web application must be listening on `0.0.0.0`, port `5000`
* Routes:
	* `/`: display “Hello HBNB!”
	* `/hbnb`: display “HBNB”
* You must use the option `strict_slashes=False` in your route definition

```
AirBnB_clone_v2(master)➜ python3 -m web_flask.1-hbnb_route
 * Serving Flask app '1-hbnb_route'
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)

-------------------------------- Terminal 2 --------------------------------
imitor＠excalibur:~$ curl 0.0.0.0:5000/hbnb ; echo "" | cat -e
HBNB$
```
- [x] *File:* [1-hbnb_route.py](1-hbnb_route.py

---
#### 2. C is fun!

**Problem:** Write a script that starts a Flask web application:

**Requirements:**
* Your web application must be listening on `0.0.0.0`, port `5000`
* Routes:
	* `/`: display “Hello HBNB!”
	* `/hbnb`: display “HBNB”
	* `/c/<text>`: display “C ” followed by the value of the `text` variable (replace underscore `_` symbols with a space ` `)
* You must use the option `strict_slashes=False` in your route definition
```
AirBnB_clone_v2(master)➜ python3 -m web_flask.2-c_route.py
 * Serving Flask app '2-c_route.py'
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)

-------------------------------- Terminal 2 --------------------------------
imitor＠excalibur:~$ curl 0.0.0.0:5000/c/is_fun ; echo "" | cat -e
C is fun$

```
- [x] *File:* [2-c_route.py](2-c_route.py)

---

#### 3. Python is cool!
**Problem:** Write a script that starts a Flask web application:

**Requirements:**
* Your web application must be listening on `0.0.0.0`, port `5000`
* Routes:
	* `/`: display “Hello HBNB!”
	* `/hbnb`: display “HBNB”
	* `/c/<text>`: display “C ” followed by the value of the `text` variable (replace underscore `_` symbols with a space ` `)
	* `/python/(<text>)`: display “Python ”, followed by the value of the `text` variable (replace underscore `_` symbols with a space ` `)
		* The default value of `text` is “is cool”
* You must use the option `strict_slashes=False` in your route definition
```
AirBnB_clone_v2(master)➜ python3 -m web_flask.3-python_route
 * Serving Flask app '3-python_route'
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)

-------------------------------- Terminal 2 --------------------------------
imitor＠excalibur:~$ curl -Ls 0.0.0.0:5000/python/is_magic ; echo "" | cat -e
Python is magic$
imitor＠excalibur:~$ curl -Ls 0.0.0.0:5000/python/ ; echo "" | cat -e 
Python is cool$
imitor＠excalibur:~$ curl -Ls 0.0.0.0:5000/python ; echo "" | cat -e 
Python is cool$
```
- [x] *File:* [3-python_route](3-python_route)

---

#### 4. Is it a number?
**Problem:** Write a script that starts a Flask web application:

**Requirements:**
* Your web application must be listening on `0.0.0.0`, port `5000`
* Routes:
	* `/`: display “Hello HBNB!”
	* `/hbnb`: display “HBNB”
	* `/c/<text>`: display “C ” followed by the value of the `text` variable (replace underscore `_` symbols with a space ` `)
	* `/python/(<text>)`: display “Python ”, followed by the value of the `text` variable (replace underscore `_` symbols with a space ` `)
		* The default value of `text` is “is cool”
	* `/number/<n>`: display “n is a number” only if `n` is an integer
* You must use the option `strict_slashes=False` in your route definition
```
AirBnB_clone_v2(master)➜ python3 -m web_flask.4-number_route.py
 * Serving Flask app '4-number_route.py'
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)

-------------------------------- Terminal 2 --------------------------------
imitor＠excalibur:~$ curl 0.0.0.0:5000/number/89 ; echo "" | cat -e
89 is a number$

imitor＠excalibur:~$ curl 0.0.0.0:5000/number/8.9
<!doctype html>
<html lang=en>
<title>404 Not Found</title>
<h1>Not Found</h1>
<p>The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.</p>

imitor＠excalibur:~$ curl 0.0.0.0:5000/number/emiwest
<!doctype html>
<html lang=en>
<title>404 Not Found</title>
<h1>Not Found</h1>
<p>The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.</p>
```
- [x] *File:* [4-number_route.py](4-number_route.py)

---

#### 5. Number template
**Problem:** Write a script that starts a Flask web application:

**Requirements:**
* Your web application must be listening on `0.0.0.0`, port `5000`
* Routes:
	* `/`: display “Hello HBNB!”
	* `/hbnb`: display “HBNB”
	* `/c/<text>`: display “C ” followed by the value of the `text` variable (replace underscore `_` symbols with a space ` `)
	* `/python/(<text>)`: display “Python ”, followed by the value of the `text` variable (replace underscore `_` symbols with a space ` `)
		* The default value of `text` is “is cool”
	* `/number/<n>`: display “n is a number” only if `n` is an integer
	* `/number_template/<n>`: display a HTML page only if n is an integer:
		* `H1` tag: “Number: n” inside the tag `BODY`
* You must use the option `strict_slashes=False` in your route definition
```
AirBnB_clone_v2(master)➜ python3 -m web_flask.5-number_template.py
 * Serving Flask app '5-number_template.py'
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
curl 0.0.0.0:5000/number_template/101 ; echo ""
<!DOCTYPE html>
<HTML lang="en">
	<HEAD>
		<TITLE>HBNB</TITLE>
	</HEAD>
	<BODY>
		<H1>Number: 101</H1>
	</BODY>
</HTML>

```
- [x] *File:* [5-number_template.py](5-number_template.py), [5-number.html](templates/5-number.html)

---

#### 6. Odd or even?
**Problem:** Write a script that starts a Flask web application:

**Requirements:**
* Your web application must be listening on `0.0.0.0`, port `5000`
* Routes:
	* `/`: display “Hello HBNB!”
	* `/hbnb`: display “HBNB”
	* `/c/<text>`: display “C ” followed by the value of the `text` variable (replace underscore `_` symbols with a space ` `)
	* `/python/(<text>)`: display “Python ”, followed by the value of the `text` variable (replace underscore `_` symbols with a space ` `)
		* The default value of `text` is “is cool”
	* `/number/<n>`: display “n is a number” only if `n` is an integer
	* `/number_template/<n>`: display a HTML page only if n is an integer:
		* `H1` tag: “Number: n” inside the tag `BODY`
	* `/number_odd_or_even/<n>`: display a HTML page only if `n` is an integer:
		* H1 tag: “Number: `n` is `even|odd`” inside the tag `BODY`
* You must use the option `strict_slashes=False` in your route definition
```
imitor＠excalibur»~➜ curl 0.0.0.0:5000/number_odd_or_even/88 ; echo ""
<!DOCTYPE html>
<HTML lang="en">
	<HEAD>
		<TITLE>HBNB</TITLE>
	</HEAD>
	<BODY>
		<H1>Number: 88 is even</H1>
	</BODY>
</HTML>
imitor＠excalibur»~➜ curl 0.0.0.0:5000/number_odd_or_even/188 ; echo ""
<!DOCTYPE html>
<HTML lang="en">
	<HEAD>
		<TITLE>HBNB</TITLE>
	</HEAD>
	<BODY>
		<H1>Number: 188 is even</H1>
	</BODY>
</HTML>
imitor＠excalibur»~➜ curl 0.0.0.0:5000/number_odd_or_even/aa ; echo ""
<!doctype html>
<html lang=en>
<title>404 Not Found</title>
<h1>Not Found</h1>
<p>The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.</p>

```
- [x] *File:* [6-number_odd_or_even.py](6-number_odd_or_even.py), [6-number_odd_or_even.html](templates/6-number_odd_or_even.html)

---

#### 7. Improve engines
**Problem:** Before using Flask to display our HBNB data, you will need to update some part of our engine:

**Requirements:**
Update `FileStorage`: (`models/engine/file_storage.py`)
* Add a public method `def close(self):`: call `reload()` method for deserializing the JSON file to objects

Update `DBStorage`: (`models/engine/db_storage.py`)
* Add a public method `def close(self):`: call `remove()` method on the private session attribute (`self.__session`) tips or `close()` on the class `Session` tips

Update `State`: (`models/state.py`) - If it’s not already present
* If your storage engine is not `DBStorage`, add a public getter method `cities` to return the list of `City` objects from `storage` linked to the current `State`
- [x] *File:* [file_storage.py](../models/engine/file_storage.py), [db_storage.py](../models/engine/db_storage.py), [state.py](../models/state.py)

---

#### 8. List of states
**Problem:** Write a script that starts a Flask web application:

**Requirements:**
* Your web application must be listening on `0.0.0.0`, port `5000`
* You must use `storage` for fetching data from the storage engine (`FileStorage` or `DBStorage`) => `from models import storage` and `storage.all(...)`
* After each request you must remove the current SQLAlchemy Session:
	* Declare a method to handle `@app.teardown_appcontext`
	* Call in this method `storage.close()`
* Routes:
	* `/states_list`: display a HTML page: (inside the tag `BODY`)
		* `H1` tag: “States”
		* `UL` tag: with the list of all State objects present in `DBStorage` sorted by `name` (A->Z) [tip](https://jinja.palletsprojects.com/en/3.0.x/templates/)
			* `LI` tag: description of one `State`: `<state.id>: <B><state.name></B>`
* Import this [7-dump](https://s3.amazonaws.com/intranet-projects-files/holbertonschool-higher-level_programming+/290/7-states_list.sql) to have some data
* You must use the option `strict_slashes=False` in your route definition

- [x] *File:* [7-states_list.py](7-states_list.py)

---

#### 9. Cities by states
**Problem:** Write a script that starts a Flask web application:

**Requirements:**
* Your web application must be listening on `0.0.0.0`, port `5000`
* You must use `storage` for fetching data from the storage engine (`FileStorage` or `DBStorage`) => `from models import storage` and `storage.all(...)`
* After each request you must remove the current SQLAlchemy Session:
	* Declare a method to handle `@app.teardown_appcontext`
	* Call in this method `storage.close()`
* Routes:
	* `/states_list`: display a HTML page: (inside the tag `BODY`)
		* `H1` tag: “States”
		* `UL` tag: with the list of all State objects present in `DBStorage` sorted by `name` (A->Z) [tip](https://jinja.palletsprojects.com/en/3.0.x/templates/)
			* `LI` tag: description of one `State`: `<state.id>: <B><state.name></B>` + `UL` tag: with the list of all State objects present in `DBStorage` sorted by `name` (A->Z) [tip](https://jinja.palletsprojects.com/en/3.0.x/templates/)
				* `LI` tag: description of one `City`: `<city.id>: <B><city.name></B>`
* Import this [7-dump](https://s3.amazonaws.com/intranet-projects-files/holbertonschool-higher-level_programming+/290/7-states_list.sql) to have some data
* You must use the option `strict_slashes=False` in your route definition

- [x] *File:* [8-cities_by_states.py](web_flask/8-cities_by_states.py), [8-cities_by_states.html](web_flask/templates/8-cities_by_states.html)

---

#### 10. States and State
**Problem:** Write a script that starts a Flask web application:

**Requirements:**
* Your web application must be listening on `0.0.0.0`, port `5000`
* You must use `storage` for fetching data from the storage engine (`FileStorage` or `DBStorage`) => `from models import storage` and `storage.all(...)`
* After each request you must remove the current SQLAlchemy Session:
	* Declare a method to handle `@app.teardown_appcontext`
	* Call in this method `storage.close()`
* Routes:
	* `/states`: display a HTML page: (inside the tag `BODY`)
		* `H1` tag: “States”
		* `UL` tag: with the list of all State objects present in `DBStorage` sorted by `name` (A->Z) [tip](https://jinja.palletsprojects.com/en/3.0.x/templates/)
			* `LI` tag: description of one `State`: `<state.id>: <B><state.name></B>` + `UL` tag: with the list of all State objects present in `DBStorage` sorted by `name` (A->Z) [tip](https://jinja.palletsprojects.com/en/3.0.x/templates/)
	* `/states/<id>`: display a HTML page: (inside the tag BODY)
		* If a `State` object is found with this `id`:
			* `H1` tag: “State: ”
			* `H3` tag: “Cities:”
			* `UL` tag: with the list of `City` objects linked to the `State` sorted by `name` (A->Z)
				* `LI` tag: description of one `City`: `<city.id>: <B><city.name></B>`
		* Otherwise:
			* `H1` tag: “Not found!”
* Import this [7-dump](https://s3.amazonaws.com/intranet-projects-files/holbertonschool-higher-level_programming+/290/7-states_list.sql) to have some data
* You must use the option `strict_slashes=False` in your route definition

- [x] *File:* [9-states.py](web_flask/9-states.py), [9-states.html](web_flask/templates/9-states.html)

---


### Advanced Task

---

#### Task_013
**Problem:** lorem_ipsum

**Requirements:**
* lorem_ipsum
* lorem_ipsum

```
code sample
```
- [ ] *File:* [Task_13](ddd)

---

#### Task_014

**Problem:** lorem_ipsum

**Requirements:**
* lorem_ipsum
* lorem_ipsum

```
code sample
```
- [ ] *File:* [Task_14](link_to_file)

---

<h2 style="text-align: center;">Collaborative Author(s)</h2>

[**Emmanuel Fasogba**](https://www.linkedin.com/in/emmanuelofasogba/)
- GitHub - [fashemma007](https://github.com/fashemma007)
- Twitter - [@tz_emiwest](https://www.twitter.com/tz_emiwest)
