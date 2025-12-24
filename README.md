# Project Management System

Backend: Django + GraphQL  
Frontend: React + TypeScript  
Database: PostgreSQL  

(multi-tenant)

## Models Implemented
- Organization
- Project
- Task
- TaskComment

Relationships:
Organization → Projects  
Project → Tasks  
Task → Comments  

Includes:
- Status fields
- Timestamps
- Proper foreign keys


## Environment & Database Setup
- Configured PostgreSQL database
- Added `.env` support using `django-environ`
- Connected Django securely with environment        variables
- Applied migrations successfully

---

## Admin Panel Setup
- Registered `Organization`, `Project`, `Task`, `TaskComment` in `admin.py`
- Added list views, filters, and searching
- Used Admin to create initial organization data

---

## GraphQL Base Integration
- Installed and configured `graphene-django`
- Enabled GraphQL endpoint at `/graphql`
- Created global schema entry in `backend/schema.py`
- Linked `CoreQuery` and `CoreMutation` from `core/schema.py`
- Enabled GraphiQL UI for testing

---

## GraphQL Types & Queries
- Created GraphQL types for all models
- Implemented core queries:
  - `projects(organizationSlug)`
  - `tasks(projectId)`
  - `comments(taskId)`
- Added organization-based data isolation (multi-tenancy)

---

## GraphQL Query Testing
- Successfully executed queries in GraphiQL
- Verified empty database returns `[]`
- Verified correct filtering by organization → project → task hierarchy

---

## Project Mutations
- Enabled global mutation support in GraphQL
- Implemented:
  - Create Project
  - Update Project
  - Delete Project
- Added validation to ensure project belongs to a valid organization

---

## Task Mutations
- Implemented:
  - Create Task
  - Update Task
  - Delete Task
- Ensures task is always linked to an existing project

---


