#!/bin/bash

if [[ $# -ne 1 ]]; then
    echo 'usage: ./install.sh <script>'
    exit 1
fi

echo "[+] Installing $1"

bash -c "$(curl -kfsSL https://raw.githubusercontent.com/senges/hax/main/scripts/$1.sh)"

echo "$1" >> /tools/.list