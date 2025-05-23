# Django Job Portal

A modern, full-featured job portal built with Django. Employers can post jobs, manage applications, and maintain company profiles. Job seekers can browse, search, and apply for jobs, track their applications, and communicate with employers.

## Features

- User authentication with separate roles: Employer & Job Seeker
- Modern, responsive Bootstrap UI
- Home page with clear login/register options
- Employer dashboard: post jobs, view/manage applications, message applicants
- Job seeker dashboard: track applications, message employers
- Company profile for employers (required to post jobs)
- Job posting with fields: title, description, location, salary, duration, job type, requirements, benefits
- Job search and filtering (title, location, employer)
- Messaging system for each application
- Application status tracking (pending, reviewed, accepted, rejected)
- Email notifications (console backend for dev)
- Admin panel for all models
- Seed command to generate demo data

## Quick Start

### 1. Clone the repository
```sh
git clone <your-repo-url>
cd job_portal
```

### 2. Create and activate a virtual environment
```sh
python -m venv venv
venv\Scripts\activate  # On Windows
# or
source venv/bin/activate  # On Mac/Linux
```

### 3. Install dependencies
```sh
pip install -r requirements.txt
```

### 4. Run migrations
```sh
python manage.py migrate
```

### 5. Seed the database with demo data
```sh
python manage.py seed_data
```

### 6. Run the development server
```sh
python manage.py runserver
```

### 7. Access the site
Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser.

## Demo Credentials

**Employers:**
- Username: `employer1` / `employer2` / `employer3`
- Password: `password123`

**Job Seekers:**
- Username: `seeker1` / `seeker2` / ...
- Password: `password123`

## File Uploads
- Uploaded resumes and company logos are stored in the `media/` directory.
- For production, configure proper media/static file serving.

## Admin Access
- Create a superuser:
  ```sh
  python manage.py createsuperuser
  ```
- Visit [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

## Customization
- Update `settings.py` for production (DEBUG, ALLOWED_HOSTS, email backend, etc.)
- Change Bootstrap theme or add your own CSS for further branding.

## Requirements
- Python 3.8+
- Django 5.x
- Pillow


**Enjoy your new job portal!**
