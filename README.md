# Flow

A Flask-based web application for managing workflow and tasks.

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd Flow
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Initialize the database:
```bash
flask db upgrade
```

6. Run the application:
```bash
python run.py
```

## Project Structure

```
Flow/
├── app/                    # Application package
│   ├── __init__.py        # Application factory
│   ├── models.py          # Database models
│   ├── routes.py          # Main routes
│   ├── forms.py           # WTForms forms
│   ├── api/               # API endpoints
│   ├── static/            # Static files (CSS, JS, images)
│   └── templates/         # Jinja2 templates
├── config/                # Configuration files
│   ├── __init__.py
│   ├── dev_config.py
│   ├── prod_config.py
│   └── test_config.py
├── deployment/           # Deployment configurations
├── docs/                # Documentation
├── instance/            # Instance-specific files
├── migrations/          # Database migrations
├── scripts/            # Utility scripts
├── tests/              # Test suite
├── .env                # Environment variables
├── .gitignore         # Git ignore rules
├── requirements.txt    # Project dependencies
└── run.py             # Application entry point
```

## Testing

Run tests with:
```bash
pytest
```

## License

[Your chosen license] 