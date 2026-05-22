#!/bin/bash

# Setting up variables
ENV='.push-express'
ENV_FILE='.env'

# Check for an existing virtual environment folder and 
# creating a venv if one does not exit

if [ ! -d "$ENV" ]; then
    echo "No virtual environment found. Creating one..."
    python3 -m venv "$ENV"
    echo "Successfully created the environment"
fi

# Check if the VIRTUAL_ENV variable is set and 
# activate the venv if not set.

if [ ! "$VIRTUAL_ENV" ]; then
    echo "Switching to the virtual environment"
    source "$ENV/bin/activate"

else
    echo "Already in the virtual environment"
fi


# Check if the requirements are already met and if not install them

if ! python3 -m pip check requirements.txt > /dev/null 2>&1; then 
    echo "Installing requirements..."
    python3 -m pip install --upgrade pip 1>/dev/null
    python3 -m pip install -r requirements.txt 1>/dev/null
    echo "Installed all dependencies"
else
    echo "All dependencies are already installed"
fi


# Check if there is an .env file and if it is empty. If either of those,
# then generate the vapid keys, add them to the .env file and delete the key files.

if [ ! -f "$ENV_FILE" ] || [ ! -s "$ENV_FILE"  ];then

    echo "No $ENV_FILE file found! Creating one"
    touch "$ENV_FILE"

    echo "Generating vapid keys..."
    vapid --gen 1>/dev/null

    # Turns the keys into a space separated list
    keys=($(python3 helpers/extract_keys.py))

    cat << EOF > "$ENV_FILE"
PRIVATE_KEY=${keys[0]}
PUBLIC_KEY=${keys[1]}
EOF

    echo "Cleaning up..."
    rm -rf *_key.pem

else
    echo "$ENV_FILE file already exists and is not empty. Skipping key generation."
fi

# Check if the backup folder exists and if not, then create the folder and 
# add an empty json file inside it.

if [ ! $(find . -type d -name "backup") ]; then

    echo "No backup folder found! Creating required folder/files..."

    mkdir "backup"
    touch backup/curDraw.json
    echo {} > backup/curDraw.json

    echo "Successfully created the folder/files..."

fi

echo "Setup Completed!"