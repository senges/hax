#!/bin/bash

apt install -y --no-install-recommends gnupg2

wget https://raw.githubusercontent.com/rapid7/metasploit-omnibus/master/config/templates/metasploit-framework-wrappers/msfupdate.erb -O /tmp/msfinstall --no-check-certificate \
    && chmod 755 /tmp/msfinstall \
    && /tmp/msfinstall \

rm -f /tmp/msfinstall \
rm -rf /var/lib/apt/lists