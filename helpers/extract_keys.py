import re


PATTERN = r"-----BEGIN[A-Z, ]+-----(.*)-----END[A-Z, ]+-----"


def extract_key(key_string):
    matches = re.match(PATTERN, key_string)

    if matches:
        return matches.group(1)

    return None


def extract_keys(file_names=None):
    if file_names is None:
        file_names = ["private_key.pem", "public_key.pem"]

    keys = []

    for file_name in file_names:
        with open(file_name, "r") as f:
            key = extract_key(f.read().replace("\n", ""))
            keys.append(key)

    return keys


if __name__ == "__main__":
    print(" ".join(extract_keys()))
