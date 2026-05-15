import re

PATTERN = r'-----BEGIN[A-Z, ]+-----(.*)-----END[A-Z, ]+-----'

def extract_key(key_string):

    matches = re.match(PATTERN,key_string)

    if matches:
        return matches.group(1)
    
    return None

if __name__ == "__main__":

    file_names = ['private_key.pem','public_key.pem']
    ret_val = []

    for file in file_names:
        
        with open(file,'r') as f:
            key = extract_key(f.read().replace("\n",""))
            ret_val.append(key)
    
    print(" ".join(ret_val))