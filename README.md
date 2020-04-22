<p align="center">
	<img src="https://user-images.githubusercontent.com/30529572/72455010-fb38d400-37e7-11ea-9c1e-8cdeb5f5906e.png" />
	<h2 align="center"> Priority Message Bot </h2>
	<h4 align="center"> Telegram bot to identify all important messages  <h4>
</p>

---
[![DOCS](https://img.shields.io/badge/license%20-MIT-green?style=flat-square&logo=appveyor)]() 
  [![UI ](https://img.shields.io/badge/built%20using%20-Python-green?style=flat-square&logo=appveyor)]()
  
## Description

Have you ever scrolled through 500 messages on a group chat to look for that one message notifying members about a very important project deadline that week or a message about an important meeting. 

Its frustrating trying to find the needle in the haystack, don't fret, we at DSC understand your woes, we have been there and done that. That's why we came up with Priority Message Bot, a contextual AI powered bot which will analyze the conversation in a telegram group in real time and keep track of all messages which might be important

And all that you have to do is ask the bot to show all those messages. Its that simple
Use this bot and never miss another important message in your telegram group

Dont beleive us? Go ahead and check out how this bot works 
## Functionalities
- [X]  Detect and track important messages
- [X]  List tracked messages on command
- [X]  Get feedback on the listed messages
- [X]  Collect additional details on important messages
- [X]  Pin the important messages
- [X]  Store important messages in database
- [X]  Retrieve stored messages and list them on command

<br>

## Run Using Docker

You can run this application using Docker

Clone the repository into your local machine.\
Then follow the steps below to create and run Docker containers of your application

1) Build a Docker image for backend API

```
cd path/to/cloned/repo/src/backend
docker build -t backend:1.0 .
```

2) Build a Docker image for telegram bot

```
cd path/to/cloned/repo/src/bot
docker build -t bot:1.0 .
```

3) Build Docker image for the reminder telegram bot

```
cd path/to/cloned/repo/src/reminder_bot
docker build -t reminderBot:1.0 .
```

3) Don't forget to add .env file in your telegram bot folder\
   Refer to **Instructions to execute** given below for the .env file sample


4) Run the containers

```
docker run --rm backend:1.0 -p 5000:5000
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

There are three components that need to be installed and run

1. The Rasa backend API which is used for NLP
2. Python script for the Priority message bot
3. Python script for the reminder bot

Clone the repository
Create a virtual environment and activate it

```bash
python3 -m venv env
source env/bin/activate
```

Install requirements for Rasa API

```bash
cd src/backend
pip install -r requirements.txt
```

Install dependencies for Telegram Bot API
The requirements for priority message bot cover the \
requirements for reminder bot

```bash
cd src/bot
pip install -r requirements.txt
```

## Instructions To Run The Application


### 1. Setting up and running Rasa API

The API endpoint for Rasa API is usually http://localhost:5000/model/parse \

We have deployed a Rasa server for you to use \
The API endpoint for it is : http://pb-rasa.herokuapp.com/model/parse

Or alternatively you can train and run a server in your computer

1. Train a Rasa NLU model

```bash
cd src/backend
rasa train nlu
```


2. Run the Rasa API Server

```bash
cd src/backend
rasa run --enable-api
```

### 2. Setting Up And Running Telegram Bots

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

## Directions To Use

Add the telegram bot to your group\
It is necessary to make the bot admin of the group.
Use the following commands to communicate with the bot

1. /show

This command makes the bot list all important messages being tracked

2. /remind

This command makes the  bot list all the important events that will occur in the next 3 days

<br>

## Screenshots of the bot

### The /show command

<img src="images/1.jpg" height="500" width="350"/>



### The tracked events can be stored by taking additional information

<img src="images/2.jpg" height="500" width="350"/>



### The stored messages can be listed

<img src="images/3.jpg" height="300" width="400"/>



## Contributors

* [  Ramaneswaran ](https://github.com/ramaneswaran)



<br>
<br>

<p align="center">
	Made with :heart: by DSC VIT
</p>

