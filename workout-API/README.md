# Secure Workout Tracker API

A lightweight, secure RESTful web service engineered with Flask for managing personalized physical logging data. The application uses stateful session handling and secure server-side validations to guarantee total operational data isolation between user accounts.

## Features
- **Stateful Authentication:** User signup, login, session validation, and logout tracking handled securely via signed secure cookies using Flask sessions.
- **Robust Model Encryption:** Database abstraction structures use `Flask-Bcrypt` for zero-plaintext password storage.
- **Secure Multitenant CRUD Operations:** Logged-in profiles retain isolated access to create, view, update, and drop only their own analytical models.
- **Data Pagination API:** The global resource retrieval pipeline automatically partitions arrays of content records into clean page indexes.

---

## Installation & Setup Instructions

### 1. Initialize Dependency Environment
Ensure Python 3.8+ is installed on your workstation, then initialize virtual mapping setups:

pipenv install
pipenv shell

### 2. Run Database Migrations
export FLASK_APP=app.py
flask db init
flask db migrate -m "Initial schema setup for users and workouts"
flask db upgrade

### 3. Seed Mock Records
python seed.py

## 4. Boot Up the Server Environment
python app.py

The API engine will default to listening on path address: http://127.0.0.1:5555

### API Documentation Endpoint Matrix

## Authentication Endpoints
* POST /register: {"username": "...", "password": "..."}, Register a brand new profile user and logs them in (status code: 201 created)

* POST /login: {"username": "...", "password": "..."}, Validates user identity parameters and maps a login session ID (status code: 200 OK)

* GET /check_session: Authenticates session status checking against state cookies (status code: 200 OK/ 401 unauthorized)

* DELETE /logout: Destroys current session profile reference context cache (status code: 204 No Contrent)

## Workout Resource Endpoints
* GET /workouts: ?page=1&per_page=5, Fetches a paginated compilation block of logged workouts for the user (status code: 200 OK)

* POST /workouts: {"title": "...", "description": "...", "duration_minutes": 60}, Generates a tracking model tied to the current account (status code: 201 created)

* PATCH /workouts/<id>: {"title": "Updated Title"}, Selectively updates mutable elements of an owned target entry (status code: 200 OK)

* DELETE /workouts/<id>: Permanently drops a specified tracking object (status code: 204 No Contrent)