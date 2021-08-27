#!/usr/bin/env python3

# Subscribes to Rapid API for stock price, read it every 20 min.
# Sends email if stock price significantly changed.

import json
import time
import datetime
import os

# For storing passwords and sensitive data as environment variables
from dotenv import load_dotenv

# For sending email
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# For retring HRRP requests if connection errors happen
import logging
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

logging.basicConfig(level=logging.DEBUG)

s = requests.Session()
retries = Retry(total=5, backoff_factor=1, status_forcelist=[ 502, 503, 504 ])
s.mount('https://', HTTPAdapter(max_retries=retries))

# Load env variables  
load_dotenv('.env')


# Safely access email and password details from .env file
class Envs:
    SENDER_EMAIL = os.getenv('SENDER_EMAIL')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    RECEIVER_EMAIL = os.getenv('RECEIVER_EMAIL') # To send to multiple recipients use "john.doe@example.com,john.smith@example.co.uk" in .env.


# Send email with formatted message either in text or html
def sendMail(stockPrice, changePercentage):
    print("Sending message")

    message = MIMEMultipart("alternative")
    message["Subject"] = "AMC is: " + str(stockPrice)
    message["From"] = Envs.SENDER_EMAIL
    message["To"] = Envs.RECEIVER_EMAIL

    # Create the plain-text or HTML version of the message
    if changePercentage <= 0.9:
        text = """Slacking down. Change is: """ + str(int((changePercentage-1)*100)) + "%."

    if changePercentage >= 1.1 <= 1.2:
        text = """Doing, good. Change is: """ + str(int((changePercentage-1)*100)) + "%."

    if changePercentage >= 1.201:
        text = """Rocking! Change is: """ + str(int((changePercentage-1)*100)) + "%."

    # Turn these into plain MIMEText objects
    part1 = MIMEText(text, "plain")
 
    # Add plain-text parts to MIMEMultipart message
    message.attach(part1)

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(Envs.SENDER_EMAIL, Envs.MAIL_PASSWORD)
        server.sendmail(
            Envs.SENDER_EMAIL, Envs.RECEIVER_EMAIL, message.as_string()
        )

    print("Message sent")


# Receive stock quote price via Rapid API interface http request
# Change AMC to another stock if needed, for eg. GME, BB, TSLA
url = "https://realstonks.p.rapidapi.com/AMC"

headers = {
    'x-rapidapi-key': os.getenv('API_KEY'),
    'x-rapidapi-host': "realstonks.p.rapidapi.com"
    }


# Main while loop
def main():
    print("\n## Subscribing to AMC stock price via API. ##\n")

    # Initialise vairiables
    t1 = 0 # 2nd time point (t-t1) 
    period = 900 # Check stock price every 15 minutes
    sleep_seconds = 300 
    price = 1 
    change = 1 # Stock change percentage

    while True:
        
        t = time.time()

        # If specified time period passed then get stock price
        if t-t1 >= period:
            response = s.get(url=url, headers=headers) # Request stock data

            if response.ok:
                data = response.json() # Convert to html data to JSON  
                output = json.loads(data)
                new_price = output['price'] # New stock price
                now = datetime.datetime.now() 
                print("Current AMC price is: ", new_price, " -- ", now.strftime("%Y-%m-%d %H:%M:%S"))
                change = abs(new_price/price)
            else: 
                print("DEBUG: Response not OK")

            t1 = time.time()

            # If stock has moved more than 10% then send email to notify
            if change >= 1.1 or change <= 0.9:
                price = new_price # Overwrite old stock price
                print("New AMC price is: ", price, " -- ", now.strftime("%Y-%m-%d %H:%M:%S"))
                sendMail(price, change)

        time.sleep(sleep_seconds) # Sleep to save system resources


if __name__ == '__main__':
    main()


