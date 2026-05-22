# This script contains the functions that help and perform the 
# polls on IRCC json file looking for changes.

import requests
import os
import re
import json
import hashlib
import constants
from datetime import datetime
from pathlib import Path

# Sets up relative structure of the backup folder from this file.

BACKUP_DIR = Path(__file__).resolve().parents[1] / "backup"

# Requests the URL of the json, generate the hash for the current json
# and compares it with the latest one that is present in the backup folder
# and returns False if there is no change. It returns the score data if 
# a change is observed.

def check_draw(logger):
    
    try:
        r = requests.get(constants.DRAW_URL)
        if r.status_code == 200:

            cur_hash = None

            if os.path.isfile(BACKUP_DIR / 'curDraw'):
                with open(BACKUP_DIR / 'curDraw','r') as f:
                    cur_hash = f.readline()
            
            new_hash = json_hash(r.json())

            if (new_hash != cur_hash):

                with open(BACKUP_DIR / 'curDraw','w') as f:
                    f.writelines(new_hash)
                
                with open(BACKUP_DIR / 'curDraw.json','w') as f:
                    json.dump(r.json(),f)

                return get_score_details(r.json())

    except requests.exceptions.RequestException as e:
        logger.error(f"An exception occurred: {e}")
    
    return False
    
# It returns a hash of a json object after normalizing it.

def json_hash(json_object):

    normalized = json.dumps(json_object,sort_keys=True,separators=(',',':'))

    return hashlib.sha256(normalized.encode('utf-8')).hexdigest()

# This grabs the data from the json and returns the required
# data in the right format.

def get_score_details(json_val):

    base_val = json_val['rounds'][0]

    normalized_pgm_name = normalize_name(base_val['drawName'])
    program_name = constants.PROGRAM_NAMES.get(normalized_pgm_name,'UKN')
    draw_date = datetime.strptime(base_val['drawDate'],'%Y-%m-%d').strftime('%m/%d/%Y')

    return {
        'program': program_name,
        'score': base_val['drawCRS'],
        'date': draw_date
    }

# A helper function that takes the program name and
# strips away everything except the actual name of the
# program.

def normalize_name(program_name):

    reString = r'([A-Za-z \-]+)'
    matches = re.match(reString,program_name)

    if (matches):
        return matches.group(1)
    else:
        program_name
