#!/bin/bash

# Install dependencies
apt install -y --no-install-recommends perl libnet-ssleay-perl

# Get nikto
git clone --depth 1 https://github.com/sullo/nikto.git /tmp/nikto
mv /tmp/nikto/program /tools/nikto

# Create PATH symbolic link
ln -s /tools/nikto/nikto.pl /tools/bin/nikto

# Cleanup
rm -rf /tmp/nikto