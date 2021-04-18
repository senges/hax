#!/bin/bash

git clone --depth 1 https://github.com/epinna/weevely3.git /tools/weevely

# Install python dependencies
pip install -r /tools/weevely/requirements.txt

# Add to PATH
ln -s /tools/weevely/weevely.py /tools/bin/weevely

# Cleanup
rm -rf /tools/weevely/{.git*,*.md,.*.yml,LICENCE,tests,requirements.txt}