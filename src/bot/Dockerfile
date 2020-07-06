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
RUN pip install cryptography
RUN pip install -r requirements.txt
RUN python -m spacy download en_core_web_sm

# Copying files
COPY . .

# Running python application
CMD ["python","app.py"]