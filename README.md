# This is README file for stock API server

## Introduction
I was frustrated not being able to find simple email notifications about stock prices so I made my own simple script for this.
Existing stock news apps sometimes fail to notify about important stock movements (think AMC and GME). 
Additionally, the notificaiton within the app on the phone can easily get lost, missed.   

## Requirements
python 3

## Instructions how to use: 
1. On a high level, there is just main.py and .env file. 
 	To start the server:
	`python3 main.py`

2. Make sure to replace variables in .env file:
	sender_email
	receiver_email
	sender_password
	api_key

3. Create Rapid API account and get key from https://rapidapi.com/
   Within Rapid API you need to subscribe to realstonks


