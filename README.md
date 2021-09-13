# Stock Price Tracker

## Introduction
This is a server developed using FastAPI for subscribing / unsubscribing clients for retreiving stock prices from RapidAPI with HTTP requests and sending email notifications to subscribers using python smtp.

## Motivation
I was frustrated with not being able to find simple email based notifications of stock prices, so I made my own script to track the stocks that I like.

Additionally, I have observed that notifications within the third-party apps can easily get lost in the phone screen and missed, but if you receive email it will be clearly visible.

Finally, existing stock news apps sometimes fail to deliver about important stock movements and it is really tiresome to be checking the stock ticker every day tracking price action (AMC and GME investors would relate to this). 


Shell:

![Alt text](images/screenshot.png?raw=true "commandline")

Localhost browser window:

![Alt text](images/screenshot1.png?raw=true "browser_window")

FatAPI docs:

![Alt text](images/screenshot2.png?raw=true "fastapi_swagger")


## Requirements
* python 3
* dotenv
* logging
* requests
* smtplib
* fastapi
* starlette
* uvicorn
* sqlalchemy
* smtplib 

## Instructions how to use: 
1. To start the server: `python3 main.py`<br />
   

2. Replace password and email variables in .env file:<br />
	`SENDER_EMAIL`, `MAIL_PASSWORD`, `API_KEY`

3. If using Gmail client you will need to enable less secure apps: https://hotter.io/docs/email-accounts/secure-app-gmail/

4. Create Rapid API account and get key from https://rapidapi.com/. Within Rapid API you need to subscribe to realstonks stock price information provider.
