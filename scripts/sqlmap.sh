#!/bin/bash

git clone --depth 1 https://github.com/sqlmapproject/sqlmap.git /tools/sqlmap

# Remove useless files
rm -rf /tools/sqlmap/.??* /tools/sqlmap/doc

# Create tool symbolic link
ln -s /tools/sqlmap/sqlmap.py /tools/bin/sqlmap