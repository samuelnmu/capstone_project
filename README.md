# capstone_project
Final Project at ALX BE
## Project Structure
ai_pamsco/                          # Project root
├── ai_pamsco/                      # Project settings package
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py                 # Global settings
│   ├── urls.py                     # Project-level routes
│   └── wsgi.py
│
├── myapp/                          # Main Django app
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py                     # App-level routes
│   ├── serializers.py              # DRF serializers
│   ├── sanitizers.py               # Custom data sanitizers
│   ├── tests.py
│   ├── templates/                  # HTML templates
│   │   └── myapp/                  # Scoped under app name
│   │       ├── base.html
│   │       ├── index.html
│   │       └── login.html
│   ├── static/                     # Static assets
│   │   └── myapp/
│   │       ├── css/
│   │       │   └── styles.css
│   │       └── js/
│   │           └── scripts.js
│   └── migrations/                 # Database migrations
│       ├── __init__.py
│       └── 0001_initial.py
│
├── manage.py                       # Django CLI
│
├── requirements.txt                # Python dependencies
└── README.md                       # Documentation


## Running ai_pamsco Project Locally

This guide will help you set up and run the project on your local machine.

1️⃣ Clone the Repository
git clone https://github.com/samuelnmu/capstone_project.git
cd capstone_project

2️⃣ Create and Activate Virtual Environment

On Linux / macOS:

python3 -m venv venv
source venv/bin/activate


On Windows (PowerShell):

python -m venv venv
venv\Scripts\activate

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Set Up Database

Run migrations to create the necessary database tables:

python manage.py makemigrations
python manage.py migrate

5️⃣ Create Environment Variables (Optional)

If your project uses environment variables (like secret keys, database configs, etc.), create a .env file in the root directory. Example:

SECRET_KEY=your_secret_key
DEBUG=True

6️⃣ Run Development Server
python manage.py runserver


Your project will now be running at:
👉 http://127.0.0.1:8000/myapp/register (This is for new users)
👉 http://127.0.0.1:8000/myapp/api/users (This is for api's)


7️⃣ Authentication (JWT)

This project uses JWT authentication with djangorestframework-simplejwt.

Get tokens: POST /api/token/

Refresh token: POST /api/token/refresh/

Verify token: POST /api/token/verify/

Use the Authorization: Bearer <access_token> header for protected routes.

8️⃣ Static Files (Optional)

If you’re serving static files locally:

python manage.py collectstatic


✅ You’re all set! The project should now be running on your local machine.


## Authorization for API
Installation

Install Django REST Framework and SimpleJWT:

pip install djangorestframework djangorestframework-simplejwt

⚙️ Configuration
1. Update settings.py

Enable REST framework authentication:

# settings.py

INSTALLED_APPS = [
    ...
    "rest_framework",
    "rest_framework.authtoken",
]

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
}

2. Configure urls.py

In your project urls.py (e.g., ai_pamsco/urls.py), add JWT endpoints:

from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("myapp/", include("myapp.urls")),  # your app routes

    # JWT Authentication endpoints
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]

 Usage with Postman
1. Obtain Tokens

Send a POST request to get the access and refresh tokens:

POST http://127.0.0.1:8000/api/token/


Request body (JSON):

{
  "username": "yourusername",
  "password": "yourpassword"
}


Response:

{
  "refresh": "long_refresh_token_here",
  "access": "short_access_token_here"
}

2. Access Protected Endpoints

Use the access token to authenticate requests.

Add a Header in Postman:

Authorization: Bearer <your_access_token>


Example:

GET http://127.0.0.1:8000/myapp/api/users/ 