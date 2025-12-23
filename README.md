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
