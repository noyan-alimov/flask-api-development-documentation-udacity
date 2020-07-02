# Basic users CRUD app

This project is a basic REST API app built with Flask. The goal of the project is to get familiar with building Back End applications with the best practices in the industry including Test Driven Development and writing Good Documentation.

All backend code follows [PEP8 style guidelines](https://www.python.org/dev/peps/pep-0008/)

## Guidelines

This is a space to write some guidelines for contributors

## Getting Started

### Pre-requisites and Local Development

Developers using this project should already have Python3, pip and node installed on their local machines.

##### Backend

From the backend folder run `pip install requirements.txt`. All required packages are included in the requirements file.

To run the application run the following commands:

- For Windows users:

```
set FLASK_APP=flaskr
set FLASK_ENV=development
flask run
```

- For Mac users:

```
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

These commands put the application in development and directs our application to use the `__init__.py` file in our flaskr folder. Working in development mode shows an interactive debugger in the console and restarts the server whenever changes are made.

The application is run on `http://127.0.0.1:5000/` by default and is a proxy in the frontend
configuration.

##### Frontend

From the frontend folder, run the following commands to start the client:

```
npm install // only once to install dependencies
npm start
```

By default, the frontend will run on localhost:3000.

##### Tests

In order to run tests navigate to the backend folder and run the following commands:

```
dropdb bookshelf_test
createdb bookshelf_test
psql bookshelf_test < books.psql
python test_flaskr.py
```

The first time you run the tests, omit the dropdb command.

All tests are kept in that file and should be maintained as updates are made to app functionality.

## API Reference

### Getting Started

- Base URL: At present this app can only be run locally and is not hosted as a base URL. This app is hosted at the default, http://127.0.0.1:5000/
- Authentication: This version of the application does not require authentication or API keys

### Error handling

Errors are returned as JSON objects in the following format:

```
{
    "success": False,
    "error": 400,
    "message": "bad request"
}
```

The API will return three error types when requests fail:

- 400: Bad Request
- 404: Resource Not Found
- 422: Not Processable

### Endpoint Library

#### GET /users

General:

- Returns a list of user objects, success value, and total number of users
- Results are paginated in groups of 3. Include a request argument to choose page number, starting from 1

Sample:
`curl http://127.0.0.1:5000/users`

```
{
  "users": [
    {
      "id": 1,
      "name": "John",
      "email": "john@mail.com"
    },
    {
      "id": 2,
      "name": "Sally",
      "email": "sally@mail.com"
    },
    {
      "id": 3,
      "name": "Ryan",
      "email": "ryan@mail.com"
    }
  ],
  "success": true,
  "total_users": 10
}
```

#### POST /users

General:

- Creates a new user using the submitted name and email. Returns the id of the created user, success value, total users and users list based on current page number to update the frontend.

Sample:
`curl http://127.0.0.1:5000/users?page=3 -X POST -H "Content-Type: application/json" -d '{"name":"Bradley", "email":"bradley@mail.com"}'`

```
{
  "users": [
    {
      "id": 7,
      "name": "Sara",
      "email": "sara@mail.com"
    },
    {
      "id": 8,
      "name": "Igor",
      "email": "igor@mail.com"
    },
    {
      "id": 9,
      "name": "Jack",
      "email": "jack@mail.com"
    }
  ],
  "created": 11,
  "success": true,
  "total_users": 11
}
```

#### DELETE /users/{user_id}

General:

- Deletes the user of the given id if it exists. Returns the id of the deleted user, success value, total users, and users list based on current page number to update the frontend.

Sample:
`curl -X DELETE http://127.0.0.1:5000/users/9?page=3`

```
{
  "users": [
    {
      "id": 7,
      "name": "Sara",
      "email": "sara@mail.com"
    },
    {
      "id": 8,
      "name": "Igor",
      "email": "igor@mail.com"
    },
    {
      "id": 10,
      "name": "Miley",
      "email": "miley@mail.com"
    }
  ],
  "deleted": 9,
  "success": true,
  "total_users": 10
}
```

#### PATCH /users/{user_id}

General:

- If provided, updates the name of the specified user. Returns the success value and the id of the modified user

Sample:
`curl http://127.0.0.1:5000/users/8 -X PATCH -H "Content-Type: application/json" -d '{"name": "Andrei"}'`

```
{
  "success": true,
  "id": 8
}
```

## Deployment N/A

## Authors

This is a space to include any authors who contributed to this project. Give credit where credit is due! If you used any open source technologies, cite those here as well.

Coach Caryn from Udacity
Student Noyan Alimov

## Acknowledgements

In the world of development, we often have thought partners who help us towards developing the best product with the best code we can. If anyone helped you on this learning journey or in developing this project specifically, give them a shout here... and let them know in real life.
