# DESCRIPTION

import os
import asyncio
import crud, models, schemas
import json
import time
import datetime

from uvicorn import *
from fastapi import FastAPI, Request, Depends, FastAPI, HTTPException
from database import SessionLocal, engine
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from typing import List
from sqlalchemy.orm import Session
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
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse

from starlette.responses import RedirectResponse


models.Base.metadata.create_all(bind=engine)

#app = FastAPI(docs_url=None, redoc_url=None)

app = FastAPI()

db1 = SessionLocal()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



logging.basicConfig(level=logging.DEBUG)

s = requests.Session()
retries = Retry(total=5, backoff_factor=1, status_forcelist=[ 502, 503, 504 ])
s.mount('https://', HTTPAdapter(max_retries=retries))

# Load env variables  
load_dotenv('.env')



# Create a new user -> subscriber
@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserBase, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

# Remove User
@app.post("/remove/", response_model=schemas.User)
def remove_subscriber(user: schemas.UserBase, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        return crud.remove_user(db=db, email=user.email)


#@app.post("/users1")
#async def root(request: Request):
#    return {"received_request_body": await request.body()}

# JSON conversion functions
@app.post("/users1")
def subscriber(email: str = Form(...)):
#    return {"email": email}
    url = "http://localhost:8000/users"
    data = {'email': email}
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    r = requests.post(url, data=json.dumps(data), headers=headers)
    return r.status_code
    
    
@app.post("/users2")
def subscriber(email: str = Form(...)):
    #return {"email": email}
    url = "http://localhost:8000/remove"
    data = {'email': email}
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    r = requests.post(url, data=json.dumps(data), headers=headers)
    print("removing user")
    return r.status_code
    #return RedirectResponse("/")

    
# Get users
@app.get("/users/", response_model=List[schemas.User])
def read_all_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
#    user_list = ""
#    for x in users:
#        print(x.email)
#        user_list += str(x.email)
#        user_list += ","
#    user_list = user_list[:-1]
#    RECEIVER_EMAIL = get_user_emails()
    return users

# Get emails as a string
def get_user_emails():
    users = crud.get_users(db1)
    user_list = ""
    for x in users:
        user_list += str(x.email)
        user_list += ","
    user_list = user_list[:-1]

    return user_list


url = "https://realstonks.p.rapidapi.com/AMC"

headers = {
    'x-rapidapi-key': os.getenv('API_KEY'),
    'x-rapidapi-host': "realstonks.p.rapidapi.com"
    }


##### Send email

# Safely access email and password details from .env file
class Envs:
    SENDER_EMAIL = os.getenv('SENDER_EMAIL')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    #RECEIVER_EMAIL = 
    #os.getenv('RECEIVER_EMAIL') # To send to multiple recipients use "john.doe@example.com,john.smith@example.co.uk" in .env.


def sendMail(stockPrice, changePercentage):

    RECEIVER_EMAIL = get_user_emails()

    print("Sending message")

    message = MIMEMultipart("alternative")
    message["Subject"] = "AMC is: " + str(stockPrice)
    message["From"] = Envs.SENDER_EMAIL
    message["To"] = RECEIVER_EMAIL

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
            Envs.SENDER_EMAIL, RECEIVER_EMAIL, message.as_string()
        )

    print("Message sent")

# Bot:
async def test():

# Initialise vairiables
    t1 = 0 # 2nd time point (t-t1) 
    period = 5 # Check stock price every 15 minutes
    sleep_seconds = 1 
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
                print(response)

            t1 = time.time()

            # If stock has moved more than 10% then send email to notify
            if change >= 1.1 or change <= 0.9:
                price = new_price # Overwrite old stock price
                print("New AMC price is: ", price, " -- ", now.strftime("%Y-%m-%d %H:%M:%S"))
                sendMail(price, change)

        await asyncio.sleep(sleep_seconds) 
        #time.sleep(sleep_seconds) # Sleep to save system resources



@app.route("/")
def form(request):
    return HTMLResponse(
        """
        <h3>Stock Tracker<h3>
        <h4>Add your email to subscriber list to track prices<h4>
        <form action="/users1" method="post" enctype="multipart/form-data"">
            <label for="email">Enter your email:</label>
            <input type="email" id="email" name="email">
            <input type="submit" value="Submit">
        </form>
        <h4>Unsubscribe:<h4>
        <form action="/users2" method="post" enctype="multipart/form-data">
            <input type="email" id="email" name="email">
            <input type="submit" value="Submit">
        </form>
    """)

@app.route("/form")
def redirect_to_homepage(request):
    return RedirectResponse("/")
    

loop = asyncio.get_event_loop()

config = Config(app=app, loop=loop)
server = Server(config)
#loop.run_until_complete(server.serve())
loop.create_task(test())


def main():
    run(
        "main:app",
        host='0.0.0.0',
    port=int(os.environ.get('PORT', 8000)),
    )
    
    
if __name__ == "__main__":
    main()
