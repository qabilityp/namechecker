# Django REST API Project

A REST API project built with Django REST Framework, featuring JWT authentication and Swagger documentation.

## 🚀 Features

- JWT Authentication
- REST API endpoints
- Swagger/ReDoc API documentation
- Docker containerization
- Pytest unit tests
- Ruff code linting

## 🛠 Tech Stack

- Python 3.12+
- Django 5.0+
- Django REST Framework
- PostgreSQL
- Docker & Docker Compose
- JWT Authentication
- Swagger/ReDoc Documentation
- Pytest
- Ruff

## 📋 Prerequisites

- Docker
- Docker Compose
- Make (optional, for using Makefile commands)

## 🔧 Environment Variables

Create a `.env` file in the root directory with the following variables:

```env
# Django
DEBUG=True
DJANGO_SECRET_KEY=your-secret-key-here
DJANGO_LOGLEVEL=info
DJANGO_ALLOWED_HOSTS=localhost,0.0.0.0,127.0.0.1,31.202.155.50

# Database
DATABASE_ENGINE=postgresql
DB_NAME=your_db_name
DATABASE_USERNAME=dbuser
DATABASE_PASSWORD=dbpassword
DATABASE_HOST=db
DATABASE_PORT=5432

# JWT
JWT_SECRET_KEY=your-jwt-secret-key

```

🚀 Getting Started

1.Clone the repository:

```
git clone https://github.com/qabilityp/namechecker.git
cd namechecker
```

2.Start the project with Docker Compose:

```
docker-compose up --build
```

3.The API will be available at:

API: http://localhost:8000/ \
Swagger UI: http://localhost:8000/api/docs/ \
ReDoc: http://localhost:8000/api/redoc/


Install dependencies:
```bash
pip install -r requirements.txt
```

## 🧹 Code Quality

### Running Ruff:
```bash
# Check code
ruff check .

# Format code
ruff format .

# Check and fix
ruff check . --fix
```

## 🧪 Running Tests

### Using Docker (recommended):
```bash
# Run tests
docker-compose run django-web python -m pytest

# Run tests with verbose output
docker-compose run django-web python -m pytest -v

# Run tests with coverage
docker-compose run django-web python -m pytest --cov
```

📝 API Endpoints

Authentication

POST /auth/register/ - Register new user

```
{
  "username": "string",
  "password": "string"
}
```
POST /auth/token/ - Obtain JWT token
```
{
  "username": "string",
  "password": "string"
}
```

Name Operations

GET /names/ - returns information about the most likely countries associated with that name
``` 
{
    "name": "Alexander",
    "likely_origins": [
        {
            "country": "Greece",
            "probability": 0.85
        },
        {
            "country": "Russia",
            "probability": 0.45
        }
    ]
}
```

GET /popular/ - returns the top 5 most frequent names associated with that country
```
{
    "country": "US",
    "top_names": [
        {
            "name": "Oliver",
            "frequency": 34215
        },
        {
            "name": "Noah",
            "frequency": 32567
        }
    ]
}
```
