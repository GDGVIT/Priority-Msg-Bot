FROM python:3.7-slim

# Check Python Environment
RUN python --version
RUN pip --version

# Set working directory for containers
WORKDIR /app

# Installing Dependencies
COPY requirements.txt .
RUN pip install pyTelegramBotAPI
RUN pip install psycopg2-binary
RUN pip install -r requirements.txt

# Copying files
COPY . .

# Running python application
CMD ["python","app.py"]