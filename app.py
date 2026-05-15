from fastapi import FastAPI
import asyncio
import os
import json
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from services.check_draws import check_draw,get_score_details
from helpers.logger import setup_logger

#Initiates Logger
logger = setup_logger()

#Creates a background task that repeats every 5 minutes to check if new draw arrived
async def backrgound_loop():
    while True:
        is_draw = check_draw()
        if is_draw:
            notify(is_draw)

        await asyncio.sleep(300)    
     
@asynccontextmanager
async def lifespan(app):

    loop = asyncio.create_task(backrgound_loop())
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

@app.get('/')
def home():
    
    if(os.path.isfile('backup/curDraw.json')):

        with open('backup/curDraw.json','r') as f:
            vals = json.load(f)

            return get_score_details(vals)
    
    else: 
        logger.ERROR(f'No json file added')

    return {'message':'Cannot access data!'}

