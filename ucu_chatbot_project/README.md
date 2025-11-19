# UCU Student Chatbot (Django + Gemini)

This project is a starter Django app that implements:
- User registration/login (Django auth)
- A simple chat UI (HTML + JS)
- A backend endpoint that calls Google Gemini (via google-genai)
- Stores chat messages in SQLite

## Setup (local dev)
1. Create a Python virtual environment and activate it:
   python -m venv venv
   source venv/bin/activate   # on Windows: venv\Scripts\activate

2. Install dependencies:
   pip install -r requirements.txt

3. Copy `.env.example` to `.env` and set values (especially GEMINI_API_KEY).

4. Run migrations and create superuser:
   python manage.py makemigrations
   python manage.py migrate
   python manage.py createsuperuser

5. Run development server:
   python manage.py runserver

6. Open http://127.0.0.1:8000/ and register/login to use chat.

## Notes
- Keep GEMINI_API_KEY secret. The app expects it to be in the environment or in `.env`.
- The view uses `gemini-2.5-flash`—change model name according to your access.
- For production, use proper secret management, HTTPS, and configure allowed hosts.

