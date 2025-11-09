# ⚙️ Task Flow – Backend

Task Flow Backend is a robust and scalable **RESTful API** built with **Django REST Framework** and **PostgreSQL**.  
It powers the Task Flow web app, enabling users to manage tasks, priorities, and due dates seamlessly.

---

## 🌐 Live API
🔗 Hosted on AWS EC2 (via Docker) and connected to the frontend at [Task Flow](https://taskflowhq.vercel.app/)

---

## 🚀 Features

- 🔒 RESTful API for task management  
- 🗓️ Create, update, and delete tasks with **due dates** and **priority levels**  
- 🧩 Structured endpoints for smooth integration with the React frontend  
- 🐳 Containerized using **Docker** for portability and scalability  
- ⚙️ Deployed on **AWS EC2** and configured with **Nginx + Gunicorn**  
- 💾 Persistent storage with **PostgreSQL**

---

## 🛠️ Tech Stack

| Area | Technology |
|------|-------------|
| Framework | Django REST Framework |
| Database | PostgreSQL |
| Deployment | Docker + AWS EC2 |
| Web Server | Nginx + Gunicorn |
| Domain | GoDaddy (Custom DNS) |

---

## ⚙️ Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/taskflow-backend.git
cd taskflow-backend
```

### 2. Create and activate a virtual environment
```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Start the development server
Create a .env file in the root directory and add:
```bash
DEBUG=True
SECRET_KEY=your_secret_key
DATABASE_NAME=taskflow_db
DATABASE_USER=postgres
DATABASE_PASSWORD=yourpassword
DATABASE_HOST=localhost
DATABASE_PORT=5432
ALLOWED_HOSTS=*
CORS_ALLOWED_ORIGINS=https://taskflowhq.vercel.app
```

### 5. Apply migrations
```bash
python manage.py migrate
```
### 6. Run the development server
```bash
python manage.py runserver
```
