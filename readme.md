# My FastAPI Project For Upwork

This is a FastAPI project designed to manage user authentication and posts. It includes functionality for user registration, login, post creation, retrieval, and deletion. The project also implements JWT-based authentication and caching for optimized performance.

## Table of Contents

- [Installation](#installation)
- [Configuration](#configuration)
- [Endpoints](#endpoints)
- [Usage](#usage)
- [Running the Project](#running-the-project)
- [Error Handling](#error-handling)


## Installation


1. Create a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

2. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Configuration

1. Set up environment variables in a `.env` file:
    ```env
    SECRET_KEY=your_secret_key
    ALGORITHM=HS256
    ACCESS_TOKEN_EXPIRE_MINUTES=30
    ```

2. Configure your database settings in `database.py`.

## Endpoints

### User Authentication

- **Signup**
    - `POST  auth/signup`
    - Request Body: 
      ```json
      {
        "email": "user@example.com",
        "password": "password"
      }
      ```

- **Login**
    - `POST auth/login`
    - Request Body:
      ```json
      {
        "email": "user@example.com",
        "password": "password"
      }
      ```

### Posts

- **Create Post**
    - `POST posts/posts`
    - Request Body:
      ```json
      {
        "text": "Your post text"
      }
      ```
    - Requires JWT token

- **Get Posts**
    - `GET posts/posts`
    - Requires JWT token

- **Delete Post**
    - `DELETE /posts/{post_id}`
    - Requires JWT token

## Usage

1. **Signup a new user**:
    - Send a `POST` request to `auth/signup` with email and password.
2. **Login**:
    - Send a `POST` request to `auth/login` with email and password to receive a JWT token.
3. **Create a post**:
    - Send a `POST` request to `posts/posts` with the post text and include the JWT token in the `Authorization` header.
4. **Get posts**:
    - Send a `GET` request to `posts/posts` with the JWT token in the `Authorization` header.
5. **Delete a post**:
    - Send a `DELETE` request to `/posts/{post_id}` with the JWT token in the `Authorization` header.

## Running the Project

1. Run the FastAPI server:
    ```bash
    uvicorn app.main:app --reload
    ```

2. Open your browser and navigate to `http://127.0.0.1:8000/docs` to access the Swagger UI for API documentation and testing.

## Error Handling

The project handles various errors and exceptions:
- **User Validation**: Ensures valid user input.
- **Database Errors**: Rolls back transactions and logs errors.
- **JWT Errors**: Validates JWT tokens and handles authentication errors.

