#!/bin/bash

apt install -y --no-install-recommends python3 python3-pip

# Set proper symbolic links to use python3
# as default python distribution

ln -s /bin/python3 /bin/python
ln -s /usr/bin/pip3 /usr/bin/pip