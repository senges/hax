#!/bin/bash

wget https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-amd64.zip -O /tmp/ngrok.zip

# Install
unzip /tmp/ngrok.zip -d /tools/bin

# Setup
rm -rf /tmp/ngrok*