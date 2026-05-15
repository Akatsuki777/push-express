#!/bin/bash

ENV='.push-express'
ENV_FILE='.env'


if [ ! -d "$ENV" ]; then
    echo "No virtual environment found. Creating one..."
    python3 -m venv "$ENV"
    echo "Successfully created the environment"
fi

if [ ! "$VIRTUAL_ENV" ];then
    echo "Switching to the virtual environment"
    source "$ENV/bin/activate"
else
    echo "All dependencies installed"
fi

if ! pip check requirements.txt > /dev/null 2>&1; then 
    echo "Installing requirements..."
    python3 -m pip install --upgrade pip 1>/dev/null
    python3 -m pip install -r requirements.txt 1>/dev/null
    echo "Installed all dependencies"
fi

if [ ! -f "$ENV_FILE" ] || [ ! -s "$ENV_FILE"  ];then

    echo "No $ENV_FILE file found! Creating one"
    touch "$ENV_FILE"

    echo "Generating vapid keys..."
    vapid --gen 1>/dev/null

    keys=($(python3 helpers/extract_keys.py))

    cat << EOF > "$ENV_FILE"
PRIVATE_KEY=${keys[0]}
PUBLIC_KEY=${keys[1]}
EOF

    echo "Cleaning up..."
    rm -rf *_key.pem

    echo "Setup Completed!"

fi
