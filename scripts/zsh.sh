#!/bin/bash

# Install zsh using `zsh-in-docker`
sh -c "$(wget -O- https://github.com/deluan/zsh-in-docker/releases/download/v1.1.1/zsh-in-docker.sh)" -- \
    -t afowler \
    -p git \ 
    -p zsh-z \
    -a 'alias vi="vim"' \
    -a 'PATH=$PATH:/tools/bin'

# Install zsh-z plugin
git clone --depth 1 https://github.com/agkozak/zsh-z.git /root/.oh-my-zsh/custom/plugins/zsh-z \
    && rm -rf /root/.oh-my-zsh/custom/plugins/zsh-z/{.git*,*.md,img,LICENSE}