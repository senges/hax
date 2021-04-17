#!/bin/bash

curl --silent "https://api.github.com/repos/tomnomnom/assetfinder/releases" \
    | grep -m 1 '"tag_name":' \
    | sed -E 's/.*"v([^"]+)".*/\1/' \
    | xargs -I@ wget https://github.com/tomnomnom/assetfinder/releases/download/v@/assetfinder-linux-amd64-@.tgz -O /tmp/assetfinder.tgz

tar -C /tools/bin/ -xvf /tmp/assetfinder.tgz

# Cleanup
rm -rf /tmp/assetfinder*