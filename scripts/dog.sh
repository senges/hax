#!/bin/bash

apt install -y --no-install-recommends gnupg2

# Download latest release
curl --silent "https://api.github.com/repos/ogham/dog/releases/latest" \
    | grep '"tag_name":' \
    | sed -E 's/.*"v([^"]+)".*/\1/' \
    | xargs -I@ wget https://github.com/ogham/dog/releases/download/v@/dog-v@-x86_64-unknown-linux-gnu.zip -O /tmp/dog.zip

mkdir -p /tmp/dog
unzip /tmp/dog.zip -d /tmp/dog

# Install
mv /tmp/dog/bin/dog /tools/bin/dog

# Add zsh plugin if installed
which zsh
if [[ $? -eq 0 ]]; then
    echo "~ adding zsh plugin"
    mkdir -p /root/.oh-my-zsh/custom/plugins/dog
    mv /tmp/dog/completions/dog.zsh /root/.oh-my-zsh/custom/plugins/dog/dog.zsh
fi

# Cleanup
rm -rf /tmp/dog