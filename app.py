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

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=['*'],
    allow_headers=['*']
)                  

@app.get('/get_data')
def get_data():
    
    if(os.path.isfile('backup/curDraw.json')):

        with open('backup/curDraw.json','r') as f:
            vals = json.load(f)

            return get_score_details(vals)
    
    else: 
        logger.ERROR(f'No json file added')

    return {'message':'Cannot access data!'}

@app.get('/vapid_key')
def get_public_key():
    return {"publicKey":constants.PUBLIC_KEY}

@app.post('/subscribe')
def add_subscriber(subscription: dict, db: Session = Depends(get_db)):
    save_subscription(db,subscription)
    return {"success":True}
