#!/bin/bash

git clone --depth 1 https://github.com/Mebus/cupp.git /tools/cupp

# Add to PATH
ln -s /tools/cupp/cupp.py /tools/bin/cupp

# Cleanup
rm -rf /tools/pydictor/{.git*,*.md,.travis.yml,LICENSE,screenshots}