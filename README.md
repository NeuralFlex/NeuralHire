# NeuralHire

Full-stack recruitment & HR platform comprising **Django backend** + **React frontend**.  
NeuralHire supports job listings, candidate tracking, ATS pipeline, dashboards, and more.

**Frontend Repo**: [NeuralFlex/NerualHire-Frontend](https://github.com/NeuralFlex/NerualHire-Frontend)  
**Backend Repo**: This is the **NeuralHire** backend  

---

## Key Features

### Backend (Django)
- REST API with role-based permissions (Admin / User)  
- Employee, Job & Candidate management  
- Authentication (JWT or token-based)  
- Salary slip / document generation  
- Dashboard data endpoints  

### Frontend (React)
- Job & Candidate views  
- ATS pipeline visualization  
- Dynamic dashboards & analytics  
- API requests via Axios  
- Routing with React Router  
- Responsive UI with Bootstrap + Tailwind  

---

## Tech Stack

| Layer     | Technology |
|-----------|-------------|
| Backend   | Django, Django REST Framework, Python |
| Frontend  | React, Axios, React Router, Tailwind, Bootstrap |
| Database  | SQLite (dev), optionally PostgreSQL for production |
| Deployment| Any cloud with support for Python + static frontends |

---

## Prerequisites

- Python 3.8+  
- Node.js (v16+) & npm / yarn  
- pip  
- (Optional) PostgreSQL if you use that instead of SQLite  

---

##  Backend Setup

Clone this repo and navigate into it:
```bash
git clone https://github.com/NeuralFlex/NeuralHire.git
cd NeuralHire
```

## Create & activate virtual environment:
```bash 
python -m venv venv
# On Linux / macOS:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

## Install backend Python dependencies:
```bash 
pip install -r requirements.txt
```

## Apply database migrations:
```bash
python manage.py migrate
```
### Create superuser:
```bash
python manage.py createsuperuser
```
### Run the backend server:
```bash
python manage.py runserver
```
The backend API will run on http://127.0.0.1:8000/ by default.