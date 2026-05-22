# A collection of helpers used throughout the app

import asyncio
import os

from dotenv import load_dotenv

import constants
from services.check_draws import check_draw
from services.push_notification import notify

# This checks if the .env file has been loaded and returns the 
# value belonging to the key.

def grab_env_var(key):
    if not os.getenv(key):
        load_dotenv()

    return os.getenv(key,None)

# This is the background_loop that continuosly polls the 
# IRCC json file to check for draws and then initiates 
# notification.

async def background_loop(logger=None):

    while True:
        is_draw = check_draw(logger)
        if is_draw:
            notify(is_draw,logger)

        await asyncio.sleep(constants.TIMER)
