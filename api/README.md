# RESTful API

## Introduction

REST, which stands for Representational State Transfer, is an architectural style used for designing networked applications. It operates over HTTP, emphasizing scalability, simplicity, and the ability to leverage the existing infrastructure of the World Wide Web.

### REST Constraints:

1. **Client-Server Architecture**: Separation of concerns between the client and server.
2. **Statelessness**: Each request from the client to the server must contain all necessary information.
3. **Cacheability**: Responses must define themselves as cacheable or non-cacheable.
4. **Uniform Interface**: A uniform way to interact with the server, which includes resource identification in requests, resource manipulation through representations, and self-descriptive messages.
5. **Layered System**: The architecture should be composed of hierarchical layers.
6. **Code on Demand (Optional)**: Servers can temporarily extend the functionality of a client by transferring executable code.

### API Definition

API stands for Application Programming Interface. It's a set of rules, protocols, and tools that allow different software applications to communicate with each other. APIs define the methods and data formats that applications can use to request and exchange information.

### CORS Explanation

CORS (Cross-Origin Resource Sharing) is a security feature implemented in browsers. It controls access to resources on a web page from another domain. It ensures that a web application running at one origin has permission to access resources from a different origin.

### HTTP Methods for RESTful APIs:

- **GET**: Used to retrieve resources.
- **POST**: Used to create resources.
- **PUT**: Used to update resources.
- **DELETE**: Used to delete resources.

### Other Types of APIs

Apart from RESTful APIs, there are other types, such as SOAP APIs, GraphQL APIs, and WebSocket APIs, each with its own design and usage patterns.

### Requesting REST APIs

To request a REST API, you typically use HTTP methods along with the appropriate endpoint URLs, headers, and sometimes, request bodies to interact with resources on a server.


## Conclusion

In summary, a REST API is a type of API that follows the principles of REST. It allows systems to communicate over the internet using standard HTTP methods.
