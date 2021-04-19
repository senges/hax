#!/bin/bash

git clone --depth=1 --branch=master https://github.com/landgrey/pydictor.git /tools/pydictor

# Add to PATH
ln -s /tools/pydictor/pydictor.py /tools/bin/pydictor

chmod +x /tools/pydictor/pydictor.py

# Cleanup
rm -rf /tools/pydictor/{.git*,*.md,LICENSE,docs}