## 🔧 Tech Stack

### Backend
- Django
- GraphQL (Graphene)
- PostgreSQL
- Django Admin
- CORS Enabled

### Frontend
- React
- TypeScript
- Apollo Client
- TailwindCSS
- Vite

---

## 🖥️ Run Locally (Without Docker)

### 1️⃣ Clone Project
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

Create `.env` inside backend:
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

Create admin:
```
python manage.py createsuperuser
```

Run server (Note: project uses port **8001**):
```
python manage.py runserver 8001
```

GraphQL:
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

Open:
http://localhost:5173

---

# 🐳 Run Using Docker

You can also run the entire system using Docker so you don’t have to install Python, Node, or PostgreSQL manually.

### 1️⃣ Clone the Repo
```
git clone <repo-url>
cd pms
```

### 2️⃣ Start Services
Make sure Docker Desktop / Docker Engine is running, then:
```
docker compose up --build -d
```
This will:
✔ Start PostgreSQL  
✔ Run Django migrations  
✔ Start Backend on **http://localhost:8001**  
✔ Start Frontend on **http://localhost:5173**  

### 3️⃣ To Stop
```
docker compose down
```
---

## 📬 Issues?
If anything breaks while starting Docker or local setup, mail with a screenshot:
📧 sahilnayak2056@gmail.com

---