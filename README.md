# DJANGO KANBAN BOARD – BACKEND API

## DESCRIPTION
This repository contains the backend API of a Kanban-style project management system.
The backend is built with Django and Django REST Framework and provides core functionality
for authentication, board management, task handling, and comments.

Frontend and backend are maintained in separate repositories.
This repository contains backend code only.


## FEATURES
- User registration and token-based authentication
- Board management with owners and members
- Task management per board
- Comment system for tasks
- Role- and permission-based access control
- Aggregated board statistics
- RESTful API built with Django REST Framework
- PEP8-compliant codebase
- Suitable for API testing with Postman or curl


## TECH STACK
- Python 3.11+
- Django 6.x
- Django REST Framework
- DRF TokenAuthentication
- SQLite (development and learning purposes)
- django-cors-headers
- Gunicorn

## Project Structure

  project/
│
├── auth_app/
├── boards_app/
├── core/
├── tasks_app/
│
├── requirements.txt
├── manage.py
└── README.md


## SETUP & INSTALLATION

### 1. Clone the repository
```bash
git clone <repository-url>
cd backend

### 2. Create a virtual environment
```bash
python -m venv venv

### Activate it:
```bash
Linux / macOS:
source venv/bin/activate

### Windows:
venv\Scripts\activate

### 3. Install dependencies
pip install -r requirements.txt

### 4. Apply database migrations
python core/manage.py migrate

### 5. Create a superuser (optional)
python core/manage.py createsuperuser

### 6. Start the development server
python core/manage.py runserver

### Server address:
http://127.0.0.1:8000/


## USAGE

### Authentication:
- Obtain a token via the login endpoint
- Include the token in all authenticated requests:
  Authorization: Token <your_token>

### Boards:
- GET /boards/
- POST /boards/
- GET /boards/{id}/
- PATCH /boards/{id}/

### Tasks:
- GET /tasks/
- POST /tasks/
- GET /tasks/{id}/
- PATCH /tasks/{id}/

### Comments:
- GET /tasks/{id}/comments/
- POST /tasks/{id}/comments/
- GET /tasks/{id}/comments/{comment_id}/
- DELETE /tasks/{id}/comments/{comment_id}/


### NOTES
- Backend-only project
- Frontend is handled in a separate repository
- SQLite is used for development purposes only
- Not intended for production use


### LICENSE
MIT License
