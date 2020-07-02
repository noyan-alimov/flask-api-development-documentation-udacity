# Getting Started

- Base URL: At present this app can only be run locally and is not hosted as a base URL. This app is hosted at the default, http://127.0.0.1:5000/
- Authentication: This version of the application does not require authentication or API keys

# Error handling

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

# Endpoint Library

### GET /users

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

### POST /users

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

### DELETE /users/{user_id}

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

### PATCH /users/{user_id}

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
