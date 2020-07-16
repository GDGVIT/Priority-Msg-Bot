# Installation And Execution

We have provided you with Dockerfiles to easily create and run Docker containers\
There is also option to use a python virtual environment to setup and run this application

Refer to the instructions given below get started

## Run Using Docker

You can run this application using Docker

Clone the repository into your local machine.\
Then follow the steps below to create and run Docker containers of your application



Build a Docker image for telegram bot

```
cd path/to/cloned/repo/src/bot
docker build -t bot:1.0 .
```

Build Docker image for the reminder telegram bot

```
cd path/to/cloned/repo/src/reminder_bot
docker build -t reminderBot:1.0 .
```

3) Don't forget to add .env file in your telegram bot folder\
   Refer to **Instructions to execute** given below for the .env file sample


4) Run the containers

```
docker run --rm bot:1.0
docker run --rm reminderBot:1.0
```

If you don't have Docker or want to tinker around with the code \
You can run them from Python virtual environments. \
Refer to the intructions below to install dependencies and run the application

## Directions To Install Dependencies

* Pre-requisites:
	-  Python >= 3.5
	-  Dependencies from requirements.txt for NLP backend and Telegram bot.

There are two python files you need to run:

1. Python script for the Priority message bot
2. Python script for the reminder bot

Clone the repository
Create a virtual environment and activate it

```bash
python3 -m venv env
source env/bin/activate
```



Install dependencies for Telegram Bot API
The requirements for priority message bot cover the \
requirements for reminder bot

```bash
cd src/bot
pip install -r requirements.txt
```

## Instructions To Run The Application

### Setting Up And Running Telegram Bots

Create a .env file in bot folder and add your credentials\
Refer to the .env file sample

#### .env File sample

BOT_TOKEN = 'YOUR TELEGRAM BOT TOKEN'

PARSER_URL = 'API ENDPOINT OF RASA SERVER'

2. Run the Telegram bot script

```bash
cd src/bot
python3 -m app.py
```

3. Also run the bot script for reminder bot

```bash
cd src/reminder_bot
python3 -m app.py
```
