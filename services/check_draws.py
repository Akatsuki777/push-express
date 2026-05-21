import requests
import re
import json
import hashlib
import constants
from datetime import datetime
from pathlib import Path

BACKUP_DIR = Path(__file__).resolve().parents[1] / "backup"

def check_draw(logger):
    
    try:
        r = requests.get(constants.DRAW_URL)
        if r.status_code == 200:
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
    
def json_hash(json_object):

    normalized = json.dumps(json_object,sort_keys=True,separators=(',',':'))

    return hashlib.sha256(normalized.encode('utf-8')).hexdigest()

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

def normalize_name(program_name):

    reString = r'([A-Za-z \-]+)'
    matches = re.match(reString,program_name)

    if (matches):
        return matches.group(1)
    else:
        program_name
