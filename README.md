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
SECRET_KEY=your-secret-key-here
DJANGO_SETTINGS_MODULE=where_from.where_from.settings

# Database
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=db
DB_PORT=5432

# JWT
JWT_SECRET_KEY=your-jwt-secret-key

```

🚀 Getting Started

1.Clone the repository:

```
git clone https://github.com/yourusername/your-repo-name.git
cd your-repo-name
```

2.Start the project with Docker Compose:

```
docker-compose up --build
```

3.The API will be available at:

API: http://localhost:8000/ \
Swagger UI: http://localhost:8000/api/docs/ \
ReDoc: http://localhost:8000/api/redoc/


🧪 Running Tests
```
# Run tests with pytest
docker-compose run web python -m pytest

# Run tests with coverage
docker-compose run web python -m pytest --cov
```

📝 API Endpoints

Authentication

POST /auth/register/ - Register new user \
POST /auth/token/ - Obtain JWT token \
POST /auth/token/refresh/ - Refresh JWT token
