import logging
import os
from datetime import datetime

def setup_logger():

    #Setup session name
    session_id = datetime.now().strftime("%Y-%m-%d_%H_%M_%S")

    #Initiate a logging instance
    logger = logging.getLogger('push-express-logger')
    logger.setLevel(logging.INFO)

    #Removes any previous instance of file handler
    for handler in list(logger.handlers):
        if isinstance(handler,logging.FileHandler):
            logger.removeHandler(handler)
            handler.close()
    
    #Create 'logs' folder if it doesnt already exist
    if not os.path.isdir('logs'):
        os.mkdir('logs')

    #Setup the handler
    fh = logging.FileHandler(f"logs/app_log_{session_id}.log")
    fh.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)

    #Add fh to logger
    logger.addHandler(fh)

    logger.info(f'********LOGGING INITIATED {session_id}********')

    return logger

