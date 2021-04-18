FROM hax:legacy

# Install python3
RUN /install.sh python3

# Install php
RUN /install.sh php

# Install mysql
RUN /install.sh mysql

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
# Broken due to libc mismatch
# RUN /install.sh dog

# Install arjun HTTP param fuzzer
RUN /install.sh arjun

# Install ffuf
RUN /install.sh ffuf

# Install assetfinder
RUN /install.sh assetfinder

# Install nikto web scanner
RUN /install.sh nikto

# Install john
RUN /install.sh john

# Install foremost
RUN /install.sh foremost

# Install nmap
RUN /install.sh nmap

ENTRYPOINT [ "/bin/zsh" ]