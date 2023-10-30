# 0x05. AirBnB clone - RESTful API
## Table of Contents
1. [Introduction](#1-introduction)
2. [Definitions](#2-definitions)
   - [What is an API?](#what-is-an-api)
   - [What is a RESTful API?](#what-is-a-restful-api)
   - [Other Types of APIs](#other-types-of-apis)
   - [What is CORS?](#what-is-cors)
3. [HTTP Methods](#3-http-methods)
   - [Retrieving Resources](#retrieving-resources)
   - [Creating a Resource](#creating-a-resource)
   - [Updating a Resource](#updating-a-resource)
   - [Deleting a Resource](#deleting-a-resource)
4. [Making Requests to a REST API](#4-making-requests-to-a-rest-api)
5. [Getting Started with Flask API](#5-getting-started-with-flask-api)
6. [Contribution & Feedback](#6-contribution--feedback)

## 1. Introduction
This project folder contains a RESTful API built with Flask. This API is designed to serve as the backend for a larger web application clone of AirBnB - HBNB

## 2. Definitions

### What is an API?
An **API (Application Programming Interface)** is a set of rules and protocols that allows different software entities to communicate with each other.

### What is a RESTful API?
**REST (Representational State Transfer)** is an architectural style for designing networked applications. A **RESTful API** uses HTTP requests to CRUD operations on data.

### Other Types of APIs:
There are several other types of APIs such as **SOAP**, **GraphQL**, **gRPC**, and **WebSocket**.

### What is CORS?
**CORS (Cross-Origin Resource Sharing)** is a security feature implemented by web browsers to prevent security issues arising when web pages make requests to different domains.

## 3. HTTP Methods

### Retrieving Resources:
**GET**: Retrieves data from the server.

### Creating a Resource:
**POST**: Submits data to the server to create a new resource.

### Updating a Resource:
**PUT** or **PATCH**: `PUT` updates the whole resource, while `PATCH` updates specific fields.

### Deleting a Resource:
**DELETE**: Deletes a resource specified by its URL.

## 4. Making Requests to a REST API
Use HTTP methods with the right endpoint. Tools like `curl` and Postman can help with this.

Example using `curl`:
```bash
# GET request
curl https://api.github.com/users/octocat

# POST request with data (replace with your endpoint)
curl -X POST -H "Content-Type: application/json" -d '{"name":"John"}' http://yourapi.com/users
```

## 5. Getting Started with Flask API

Here's a small Flask project to showcase an API:

```python
from flask import Flask, jsonify

app = Flask(__name__)

# Sample data
users = [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]

@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(users)

@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = next((u for u in users if u['id'] == id), None)
    if user:
        return jsonify(user)
    return jsonify({"message": "Not Found"}), 404

if __name__ == "__main__":
    app.run(debug=True)
```

To interact with this API, simply start the Flask app and use a tool like `curl` or a browser to make requests to `http://localhost:5000/users`.

---