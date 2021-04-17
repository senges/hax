#!/bin/bash

curl --silent "https://api.github.com/repos/ffuf/ffuf/releases/latest" \
    | grep '"tag_name":' \
    | sed -E 's/.*"v([^"]+)".*/\1/' \
    | xargs -I@ wget https://github.com/ffuf/ffuf/releases/download/v@/ffuf_@_linux_amd64.tar.gz -O /tmp/ffuf.tar.gz

mkdir -p /tmp/ffuf

tar -C /tmp/ffuf -xzvf /tmp/ffuf.tar.gz 
mv /tmp/ffuf/ffuf /tools/bin/ffuf

# Cleanup
rm -rf /tmp/ffuf*