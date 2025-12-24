# Mini Project Management System

This is a practical multi-tenant project management system built to demonstrate real-world backend and frontend engineering.  

---

## 1. Tech Stack

### Backend
- Django
- GraphQL (Graphene)
- PostgreSQL
- Django Admin
- CORS handled

### Frontend
- React
- TypeScript
- Apollo Client
- TailwindCSS
- Vite

---

## 2. Local Setup Guide

### Clone Repository
```
git clone <repo-url>
cd pms
```

---

## Backend Setup
```
cd backend
python -m venv venv
source venv/bin/activate       (Linux / Mac)
venv\Scripts\activate        (Windows)
pip install -r requirements.txt
```

Create PostgreSQL database:
```
CREATE DATABASE pms_db;
```

Create `.env` in backend:
```
DB_NAME=pms_db
DB_USER=postgres
DB_PASS=yourpassword
DB_HOST=localhost
DB_PORT=5432
```

Run migrations:
```
python manage.py migrate
```

Create admin user:
```
python manage.py createsuperuser
```

Run backend:
```
python manage.py runserver 8001
```

GraphQL Endpoint:
http://localhost:8001/graphql

Admin Panel:
http://localhost:8001/admin

---

## Frontend Setup
```
cd frontend
npm install
npm run dev
```

Open in browser:
http://localhost:5173

---

## 3. Folder Structure and Features Together

---

## Backend
```
backend/
```
This is responsible for business logic, database, and GraphQL API.

### Models (Database Layer)
Location:
```
backend/core/models.py
```
Contains:
- Organization
- Project
- Task
- TaskComment

Data flow:
Organization → Projects  
Project → Tasks  
Task → Comments  

Multi-tenancy is handled using `organization.slug`.

---

### GraphQL (API Layer)
Location:
```
backend/core/schema.py
```

Provides:

#### Queries
- List organizations
- List projects by organization
- List tasks by project
- List comments by task

#### Mutations
- Create / update / delete project
- Create / update / delete task
- Add / delete task comments

#### Project Statistics
For each project, backend calculates:
- total tasks
- completed tasks
- in-progress tasks
- todo tasks
- completion percentage

---

## Frontend
```
frontend/
```
This handles everything the user interacts with.

---

### Apollo Client
```
frontend/src/apollo/client.ts
```
Connects React app with Django GraphQL API.

---

### GraphQL Queries and Mutations
```
frontend/src/graphql/
```
Defines how frontend talks to backend.

---

### Pages
```
frontend/src/pages/
```

#### Projects Page
- User enters organization slug
- Projects are fetched dynamically
- Displays project list

#### Project Details Page
- Shows project statistics
- Displays tasks
- Shows status
- Shows comments

---

## What the System Can Do

- Supports multiple organizations safely
- Handles project lifecycle
- Allows task creation and updates
- Supports commenting on tasks
- Shows project progress clearly
- Clean backend and frontend separation
- Production-like folder structure
- Simple but realistic system