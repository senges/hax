FROM ubuntu:latest

ARG DEBIAN_FRONTEND=noninteractive

# Create tools folder
RUN mkdir -p /tools/bin

# Add install script
COPY ./scripts/install.sh /install.sh
RUN chmod +x /install.sh

# Install common packages
RUN apt update \
    && apt install -y --no-install-recommends tzdata git wget curl zip unzip vim iputils-ping netcat dnsutils tree
    # && rm -rf /var/lib/apt/lists/

# Install python3 properly
RUN /install.sh python3

# Install php
RUN /install.sh php

# Install zsh
RUN /install.sh zsh

# Install exiftool
RUN /install.sh exiftool

# Install sqlmap
RUN /install.sh sqlmap

# Install dirsearch
RUN /install.sh dirsearch

# Download searchsploit (but remove heavy local exploit files)
RUN /install.sh searchsploit.min

# Install sherlock
RUN /install.sh sherlock

# Install dog DNS tool
# Boken due to libc mismatch
# RUN /install.sh dog

# Install arjun HTTP param fuzzer
RUN /install.sh arjun

# Install ffuf
RUN /install.sh ffuf

# Add
#   mysql
#   Wordlists

WORKDIR "/root"