# Task Manager API
~ By Sagar Kundu🙂

A simple Task Manager API built with Django and Django REST Framework (DRF) with JWT authentication.

## Features
- User Registration and Authentication using JWT
- Task CRUD operations (Create, Read, Update, Delete)
- Pagination and Filtering
- Admin Task Management

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/sa001gar/Task-Management-API.git
   cd Task-Management-API/task_manager/
   ```
2. Create a virtual environment and activate it:
   ```sh
   python -m venv venv
   source venv/bin/activate # On Windows use `venv\Scripts\activate`
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. Run database migrations:
   ```sh
   python manage.py migrate
   python manage.py makemigrations
   ```
5. Create a superuser:
   ```sh
   python manage.py createsuperuser
   ```
6. Run the development server:
   ```sh
   python manage.py runserver
   ```

## Authentication
The API uses JWT for authentication. To get a token:
```sh
curl -X POST http://127.0.0.1:8000/api/v1/token/ -H "Content-Type: application/json" -d '{"username": "your_username", "password": "your_password"}'
```
This will return an access and refresh token. Use the access token in your requests:
```sh
Authorization: Bearer YOUR_ACCESS_TOKEN
```

## API Endpoints

### User Registration
**Endpoint:** `/api/v1/user/register/`
- **Method:** POST
- **Request Body:**
  ```json
  {
    "username": "newuser",
    "password": "newpass123"
  }
  ```
- **Response:**
  ```json
  {
    "message": "User registered successfully"
  }
  ```

### Get JWT Token
**Endpoint:** `/api/v1/token/`
- **Method:** POST
- **Request Body:**
  ```json
  {
    "username": "your_username",
    "password": "your_password"
  }
  ```
- **Response:**
  ```json
  {
    "access": "your_access_token",
    "refresh": "your_refresh_token"
  }
  ```

### Refresh Token
**Endpoint:** `/api/v1/token/refresh/`
- **Method:** POST
- **Request Body:**
  ```json
  {
    "refresh": "your_refresh_token"
  }
  ```

### Task Management

#### List Tasks (Paginated)
**Endpoint:** `/api/v1/tasks/`
- **Method:** GET
- **Headers:**
  ```sh
  Authorization: Bearer YOUR_ACCESS_TOKEN
  ```
- **Response:**
  ```json
  {
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
      {
        "id": 1,
        "title": "Test Task",
        "description": "Task description",
        "completed": false,
        "created_at": "2024-03-17T12:00:00Z"
      }
    ]
  }
  ```

#### Create Task
**Endpoint:** `/api/v1/tasks/`
- **Method:** POST
- **Headers:**
  ```sh
  Authorization: Bearer YOUR_ACCESS_TOKEN
  ```
- **Request Body:**
  ```json
  {
    "title": "New Task",
    "description": "Task details",
    "completed": false
  }
  ```

#### Retrieve Task
**Endpoint:** `/api/v1/tasks/{id}/`
- **Method:** GET
- **Headers:**
  ```sh
  Authorization: Bearer YOUR_ACCESS_TOKEN
  ```

#### Update Task
**Endpoint:** `/api/v1/tasks/{id}/`
- **Method:** PATCH
- **Headers:**
  ```sh
  Authorization: Bearer YOUR_ACCESS_TOKEN
  ```
- **Request Body:**
  ```json
  {
    "title": "Updated Task"
  }
  ```

#### Delete Task
**Endpoint:** `/api/v1/tasks/{id}/`
- **Method:** DELETE
- **Headers:**
  ```sh
  Authorization: Bearer YOUR_ACCESS_TOKEN
  ```

## cURL Commands

### Register a New User
```sh
curl -X POST http://127.0.0.1:8000/api/v1/user/register/ \
     -H "Content-Type: application/json" \
     -d '{"username": "newuser", "password": "newpass123"}'
```

### Get JWT Token
```sh
curl -X POST http://127.0.0.1:8000/api/v1/token/ \
     -H "Content-Type: application/json" \
     -d '{"username": "your_username", "password": "your_password"}'
```

### List Tasks
```sh
curl -X GET http://127.0.0.1:8000/api/v1/tasks/ \
     -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Create Task
```sh
curl -X POST http://127.0.0.1:8000/api/v1/tasks/ \
     -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"title": "New Task", "description": "Task details", "completed": false}'
```

### Retrieve Task
```sh
curl -X GET http://127.0.0.1:8000/api/v1/tasks/1/ \
     -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Update Task
```sh
curl -X PATCH http://127.0.0.1:8000/api/v1/tasks/1/ \
     -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"title": "Updated Task"}'
```

### Delete Task
```sh
curl -X DELETE http://127.0.0.1:8000/api/v1/tasks/1/ \
     -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Running Tests
To run the test cases:
```sh
python manage.py test
```

## Deployment
To deploy the application:
```sh
pip install gunicorn
python manage.py collectstatic
```
Use Gunicorn to serve the app:
```sh
gunicorn task_manager.wsgi:application --bind 0.0.0.0:8000
```
Now Configure Nginx or any web server and you are good to go.

## Docker


