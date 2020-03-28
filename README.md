<p align="center">
	<img src="https://user-images.githubusercontent.com/30529572/72455010-fb38d400-37e7-11ea-9c1e-8cdeb5f5906e.png" />
	<h2 align="center"> Priority Message Bot </h2>
	<h4 align="center"> Telegram bot to identify all important messages  <h4>
</p>

---
[![DOCS](https://img.shields.io/badge/Documentation-see%20docs-green?style=flat-square&logo=appveyor)](INSERT_LINK_FOR_DOCS_HERE) 
  [![UI ](https://img.shields.io/badge/User%20Interface-Link%20to%20UI-orange?style=flat-square&logo=appveyor)](INSERT_UI_LINK_HERE)


## Functionalities
- [X]  Detect and track important messages
- [X]  List tracked messages on command
- [X]  Get feedback on the listed messages
- [X]  Collect additional details on important messages

<br>



## Directions To install

* Pre-requisites:
	-  Python >= 3.5
	-  Dependencies from requirements.txt for NLP backend and Telegram bot.

There are two components that need to be installed and run

1. The Rasa backend API which is used for NLP
2. Python script for the Telegram bot

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

```bash
cd src/bot
pip install -r requirements.txt
```

## Instructions to execute

### Directions to run

Create a .env file and add your credentials\
Refer to the .env file sample

#### .env File sample

BOT_TOKEN = 'YOUR TELEGRAM BOT TOKEN'

PARSER_URL = 'API ENDPOINT OF RASA SERVER'


1. Run the Rasa API Server

```bash
cd src/backend
rasa run --enable-api
```

2. Run the Telegram bot script

```bash
cd src/bot
python3 -m app.py
```

### Direction To Use

Add the telegram bot to your group\
Use the following commands to communicate with the bot

1. /start

This command activates the bot, now the bot will listen to all messages

2. /show

This command makes the bot list all important messages being tracked

<br>

## Contributors

* [  Ramaneswaran ](https://github.com/ramaneswaran)



<br>
<br>

<p align="center">
	Made with :heart: by DSC VIT
</p>

