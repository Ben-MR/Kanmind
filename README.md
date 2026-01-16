# Django Kanban Board – Backend (DRF)

This repository contains the **backend** of a simple Kanban/board system built with **Django** and **Django Rest Framework**.  
The project is intended as a **practice project** and deliberately uses **SQLite** as the database.

The frontend consists of static HTML/JavaScript files and is maintained separately from the backend.

---

## Features

- User registration and login (token-based authentication)
- Email-based login (email = username)
- Boards with:
  - Owner (creator)
  - Members (many-to-many)
- Tasks per board
- Access control:
  - Only owners or members can access a board
- Aggregated board data:
  - Member count
  - Total task count
  - TODO task count
  - High-priority task count
- REST API using Django Rest Framework

---

## Tech Stack

- Python 3.11+
- Django 6.x
- Django Rest Framework
- SQLite (for practice purposes)
- DRF TokenAuthentication
- django-cors-headers
- Gunicorn (deployment)

---

## Project Structure

```text
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
