#!/bin/bash

git clone --depth 1 https://github.com/maurosoria/dirsearch.git /tools/dirsearch
pip install -r /tools/dirsearch/requirements.txt

# Cleanup
rm -rf /tools/dirsearch/.??*

# Add to PATH
ln -s /tools/dirsearch/dirsearch.py /tools/bin/dirsearch