#!/bin/bash

# Install dependencies
apt install -y --no-install-recommends perl perl-net-ssleay

# Get nikto
git clone --depth 1 https://github.com/sullo/nikto /tmp/nikto
mv /tmp/nikto/program /tools/nikto

# Create PATH symbolic link
ln -s /tools/nikto/nikto.pl /tools/nikto

# Cleanup
rm -rf /tmp/nikto