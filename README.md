# 🎉 Event Management API (Django + DRF)

An Event Management System built with **Django** and **Django REST Framework (DRF)** that allows users to:

- Create, update, and delete events  
- RSVP to events (Going, Maybe, Not Going)  
- Leave event reviews with ratings  
- Restrict access to private events (only invited users can view)  
- Authenticate via JWT tokens  
- Optionally send email reminders using Celery + Redis  

---

## 🧠 Features

✅ **Event Management**
- Create, list, update, delete events  
- Public and private event visibility  
- Organizer-only edit/delete permissions  

✅ **RSVP System**
- RSVP to events (Going, Maybe, Not Going)  
- Update RSVP status  

✅ **Review System**
- Leave a 1–5 star rating and comment  
- Prevent duplicate reviews per event  

✅ **Authentication**
- JWT-based login and token refresh  
- Authenticated users can manage their events  

✅ **Filtering, Search & Pagination**
- Filter events by organizer, location, or visibility  
- Search by title, location, or organizer username  
- Paginated responses (10 items per page)  

✅ **Celery Integration (Optional)**
- Asynchronous email reminders to invited users  

---

## 🧩 Tech Stack

| Component | Technology |
|------------|-------------|
| Backend | Django 4.x |
| API | Django REST Framework |
| Auth | JWT (via SimpleJWT) |
| Async Tasks | Celery + Redis |
| Database | SQLite / PostgreSQL |
| Documentation | DRF YASG (Swagger) |

---

## ⚙️ Installation & Setup

### 1️⃣ Clone Repository
```bash
git clone https://github.com/yourusername/Event-Management-in-DRF.git
cd Event-Management-in-DRF

python -m venv eventmvenv
# Activate
eventmvenv\Scripts\activate  # On Windows
# OR
source eventmvenv/bin/activate  # On macOS/Linux

pip install -r requirements.txt

python manage.py makemigrations
python manage.py migrate

python manage.py createsuperuser

python manage.py runserver
```
🔗 To find all api urls type command
```
python manage.py show_urls
```
🕒 Asynchronous Tasks (Celery)
To enable background email reminders:
```
Ensure Redis is running (redis://localhost:6379/0)
```
```
Start Celery workers:
```
celery -A project worker -l info
celery -A project beat -l info
