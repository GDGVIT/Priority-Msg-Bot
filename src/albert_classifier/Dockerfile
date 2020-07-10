FROM python:3.7-slim

# Check Python Environment
RUN python --version
RUN pip --version

# Set working directory for containers
WORKDIR /app

# Installing Dependencies
COPY requirements.txt .
RUN pip install gunicorn
RUN pip install -r requirements.txt

# Copying files
COPY . .

# Running python application
CMD gunicorn app:app --bind 0.0.0.0:$PORT --reload