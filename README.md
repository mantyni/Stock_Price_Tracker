# This is README file for stock API server

## Introduction
I was frustrated not being able to find simple email notifications for stock prices so I made my own script for this.
Existing stock news apps sometimes fail to notify about important stock movements (think AMC and GME). 
Additionally, the notificaiton within the app on the phone can easily get lost, missed, but email message will not. 

![Alt text](images/screenshot.png?raw=true "StockPriceServer")

## Requirements
python 3
dotenv
logging
requests
smtplib

## Instructions how to use: 
1. On a high level, there is just main.py and .env file.<br />
 	To start the server: `./main.py`<br />
	Make sure the file is executable (`chmod +x main.py`)

2. Replace password and email variables in .env file:<br />
	`SENDER_EMAIL`, `RECEIVER_EMAIL`, `MAIL_PASSWORD`, `API_KEY`

3. If using Gmail client you will need to enable less secure apps: https://hotter.io/docs/email-accounts/secure-app-gmail/

4. Create Rapid API account and get key from https://rapidapi.com/. Within Rapid API you need to subscribe to realstonks.
