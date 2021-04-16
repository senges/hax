#!/bin/bash

if [[ $# -ne 1 ]]; then
    echo 'usage: ./install.sh <script>'
    exit 1
fi

echo "[+] Installing $1"

sh -c "$(curl -kfsSL https://raw.githubusercontent.com/senges/hax/main/scripts/$1.sh)"