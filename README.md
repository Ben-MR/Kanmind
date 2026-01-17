Django Kanban Board – Backend API
Description

This repository contains the backend API of a Kanban-style project management system.
The backend is built with Django and Django REST Framework and provides all core functionality for user authentication, board and task management, and comment handling.

Frontend and backend are maintained in separate repositories.
This repository contains backend code only.

Features

User registration and authentication (token-based)

Board management with owners and members

Task management per board

Comment system for tasks

Role- and permission-based access control

Aggregated board statistics (task counts, priorities)

RESTful API using Django REST Framework

Follows PEP8 coding standards

Ready for testing with Postman or curl

Tech Stack

Python 3.11+

Django 6.x

Django REST Framework

DRF TokenAuthentication

SQLite (used intentionally for development and learning)

django-cors-headers

Gunicorn (deployment)

Project Structure
backend/
├── db.sqlite3
├── core/
│   ├── manage.py
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── user_auth_app/
├── boards_app/
├── tasks_app/
├── static/
└── requirements.txt

Setup & Installation
1. Clone the repository
git clone <repository-url>
cd backend

2. Create and activate a virtual environment
python -m venv venv


Activate it:

Linux / macOS:

source venv/bin/activate


Windows:

venv\Scripts\activate

3. Install dependencies
pip install -r requirements.txt

4. Apply database migrations
python core/manage.py migrate


SQLite is used by default. No additional database configuration is required.

5. Create a superuser (optional)
python core/manage.py createsuperuser

6. Start the development server
python core/manage.py runserver


The server will be available at:

http://127.0.0.1:8000/

Usage
Authentication

Authentication is handled via token-based authentication

Obtain a token via the login endpoint

Include the token in all authenticated requests:

Authorization: Token <your_token>

Boards

List boards: GET /boards/

Create board: POST /boards/

Board detail: GET /boards/{id}/

Update board: PATCH /boards/{id}/

Tasks

List tasks: GET /tasks/

Create task: POST /tasks/

Task detail: GET /tasks/{id}/

Update task: PATCH /tasks/{id}/

Comments

List comments for a task: GET /tasks/{id}/comments/

Create comment: POST /tasks/{id}/comments/

Comment detail: GET /tasks/{id}/comments/{comment_id}/

Delete comment: DELETE /tasks/{id}/comments/{comment_id}/

Environment Variables

Create a .env file in the project root if required:

DEBUG=True
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=127.0.0.1,localhost


Do not commit .env files or database files to version control.

Notes

Backend-only project

Frontend is handled in a separate repository

SQLite is used for development purposes only

Not intended for production use

License

This project is licensed under the MIT License.
