# Current Project Structure

```
├── app/                            # Core application code
│   ├── __init__.py                # Flask app initialization
│   ├── api/                       # API endpoints
│   │   ├── __init__.py            # API blueprint initialization
│   │   └── resources.py           # API resource definitions
│   ├── auth.py                    # Authentication logic
│   ├── extensions.py              # Flask extensions initialization
│   ├── forms.py                   # Form definitions
│   ├── models.py                  # Database models
│   ├── routes.py                  # Web routes
│   ├── static/                    # Static assets
│   │   ├── css/                   # Stylesheets
│   │   │   └── styles.css         # Main CSS file
│   │   ├── images/                # Image assets
│   │   └── js/                    # JavaScript files
│   │       └── main.js            # Main JS file
│   └── templates/                 # HTML templates
│       ├── base.html              # Base template
│       ├── dashboard.html         # Dashboard page
│       ├── index.html             # Homepage
│       ├── login.html             # Login page
│       └── tasks.html             # Tasks page
├── config/                        # Configuration files
│   ├── __init__.py                # Config package initialization
│   ├── dev_config.py              # Development settings
│   ├── prod_config.py             # Production settings
│   └── test_config.py             # Test settings
├── deployment/                    # Deployment configurations
│   ├── Dockerfile                 # Docker build instructions
│   ├── README.md                  # Deployment documentation
│   ├── docker-compose.yml         # Docker Compose config
│   └── k8s/                       # Kubernetes configs
│       ├── deployment.yaml        # K8s deployment
│       └── service.yaml           # K8s service
├── docs/                          # Project documentation
│   ├── Dashboard Design.md        # Dashboard design specs
│   ├── Database_Schema.md         # Database schema docs
│   ├── Flow App User Stories.md   # User stories
│   ├── Flow Task Management API.md # API documentation
│   ├── Flow Task Management Models.md # Data models docs
│   ├── Index.md                   # Documentation index
│   ├── Login Auth Document.md     # Authentication docs
│   ├── Structure.md               # Original structure doc
│   └── Tasks_Page.md              # Tasks page specs
├── instance/                      # Instance-specific files
│   └── flow.db                    # SQLite database
├── migrations/                    # Database migrations
├── postman/                       # API testing
│   └── Flow_API_Collection.json   # Postman collection
├── scripts/                       # Utility scripts
│   ├── init_db.py                 # Database initialization
│   ├── query_tasks.py             # Task querying script
│   ├── query_tasks.sh             # Task query shell script
│   ├── seed_data.py              # Data seeding script
│   ├── seed_db.sh                # Database seeding shell script
│   └── validate_schema.py        # Schema validation
├── tests/                        # Test suite
│   ├── __init__.py               # Test package initialization
│   └── test_example.py           # Example tests
├── uploads/                      # File upload directory
├── Index.md                      # Project index
├── README.md                     # Project readme
├── requirements.txt              # Python dependencies
└── run.py                        # Application entry point
``` 