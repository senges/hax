#!/bin/bash

git clone --depth 1 https://github.com/sherlock-project/sherlock.git /tmp/sherlock
pip install -r /tmp/sherlock/requirements.txt
mv /tmp/sherlock/sherlock /tools/sherlock

# Add to PATH
ln -s /tools/sherlock/sherlock.py /tools/bin/sherlock
chmod +x /tools/sherlock/sherlock.py

# Cleanup
rm -rf /tmp/sherlock