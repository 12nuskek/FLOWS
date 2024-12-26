# Flow - Task Management Application

A Django-based task management application with user management, dashboard, and settings functionality.

## Features

- User Authentication (Login/Logout)
- Dashboard
- User Settings
- Modern Bootstrap UI

## Setup

1. Create a virtual environment:
```bash
python3 -m venv venv
```

2. Activate the virtual environment:
```bash
source venv/bin/activate  # On Unix/macOS
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Create a superuser (admin):
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

The application will be available at http://127.0.0.1:8000/

## Usage

- Visit the homepage at `/`
- Login at `/accounts/login/`
- Access your dashboard at `/dashboard/`
- Manage your settings at `/settings/`

## Development

The project structure is organized as follows:

- `flow/` - Main project directory
- `core/` - Main application
- `templates/` - HTML templates
- `static/` - Static files (CSS, JavaScript)

## License

MIT License 