# Use the official Python runtime image
FROM python:3.13-slim

# Create the app directory

# Set the working directory inside the container
WORKDIR /app

# Set environment variables
# Prevents Python from writing pyc files to disk
ENV PYTHONDONTWRITEBYTECODE=1
#Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED=1

# Upgrade pip
RUN pip install --upgrade pip

# Copy the Django project  and install dependencies
COPY requirements.txt .

# run this command to install all dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install pytest pytest-django pytest-asyncio httpx

# Copy the Django project to the container
COPY . .

ENV PYTHONPATH=/app

RUN adduser --disabled-password --gecos '' appuser && chown -R appuser /app
USER appuser

# Expose the Django port
EXPOSE 8000

# Run Django’s development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]