#!/bin/bash

git clone --depth=1 --branch=master https://github.com/landgrey/pydictor.git /tools/pydictor

# Waiting for my PR to be merged on the official repo.
# This is a temporary patch.
sed -i '21s/abspath/realpath/' /tools/pydictor/lib/data/data.py
sed -i '22s/abspath/realpath/' /tools/pydictor/lib/data/data.py

# Add to PATH
ln -s /tools/pydictor/pydictor.py /tools/bin/pydictor

chmod +x /tools/pydictor/pydictor.py

# Cleanup
rm -rf /tools/pydictor/{.git*,*.md,LICENSE,docs}