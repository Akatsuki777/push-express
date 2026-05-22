# Main app

from fastapi import FastAPI, Depends
import asyncio
import os
import sys
import json
from sqlalchemy.orm import Session
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from services.check_draws import get_score_details
from helpers.logger import setup_logger 
from helpers.utils import background_loop
import constants
from database import engine, Base, SessionLocal
from models.subscriptions import PushSubscription
from services.push_notification import save_subscription

#Setup the Database
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

#Initiates Logger
logger = setup_logger()

# Sets the lifespan of the app which will start the background_loop 
# before the app starts and then stop it when quitting.

@asynccontextmanager
async def lifespan(app):

    loop = asyncio.create_task(background_loop(logger))
    logger.info("Background Task Created!")

    yield

    loop.cancel()

    try: 
        await loop
    except asyncio.CancelledError:
        pass

# Initiate the FastAPI instance
app = FastAPI(lifespan=lifespan)

# Allow cross origin access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=['*'],
    allow_headers=['*']
)                  

# Get the latest available data on the draws. 
# Returns error if data not available.

@app.get('/get_data')
def get_data():
    
    if(os.path.isfile('backup/curDraw.json')):

        with open('backup/curDraw.json','r') as f:
            vals = json.load(f)

            return get_score_details(vals)
    
    else: 
        logger.ERROR(f'No json file added')

    return {'message':'Cannot access data!'}

# Getter for the vapid_key

@app.get('/vapid_key')
def get_public_key():
    return {"publicKey":constants.PUBLIC_KEY}

# Endpoint that initiates the subscription process.

@app.post('/subscribe')
def add_subscriber(subscription: dict, db: Session = Depends(get_db)):
    save_subscription(db,subscription)
    return {"success":True}
