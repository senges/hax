#!/bin/bash

git clone --depth 1 https://github.com/offensive-security/exploitdb.git /tools/exploitdb

# Cleanup
rm -rf /tools/exploitdb/.git* /tools/exploitdb/exploits /tools/exploitdb/shellcodes /tools/exploitdb/*.md

# Add to PATH
ln -s /tools/exploitdb/searchsploit /tools/bin/searchsploit

# Make shortcut to download exploit
# => Not yet working
#
# searchsploit() {
#     echo 
#     if [[ "$#" -ge 2 && "$1" == "dl" ]]; then
#         wget "https://www.exploit-db.com/download/$2"
#     else
#         /tools/exploitdb/searchsploit "$1"
#     fi
# }