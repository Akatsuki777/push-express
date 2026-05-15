import requests
import json
import hashlib
from dotenv import load_dotenv
from constants import Constants

def check_draw(logger):
    
    try:
        r = requests.get(Constants.DRAW_URL)
        if r.status_code() == 200:
            with open('../backup/curDraw','r') as f:
                cur_hash = f.readline()
            
            new_hash = json_hash(r.json())

            if (new_hash != cur_hash):
                with open('../backup/curDraw','w') as f:
                    f.writelines(new_hash)
                
                with open('../backup/curDraw.json','w') as f:
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

    return {
        'program': base_val['drawName'],
        'score': base_val['drawCRS'],
        'count': base_val['drawSize']
    }
