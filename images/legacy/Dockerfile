FROM ubuntu:latest

ARG DEBIAN_FRONTEND=noninteractive

# Create tools folder
RUN mkdir -p /tools/bin

# Add install script
COPY ../../script/install.sh /install.sh
RUN chmod +x /install.sh

# Install common packages
RUN apt update \
    && apt install -y --no-install-recommends tzdata git wget curl zip vim iputils-ping netcat dnsutils tree \
    && apt install -y --no-install-recommends python3 python3-pip \
    && apt install -y --no-install-recommends php-cli php-curl php-json php-zip \
    && apt install -y --no-install-recommends nmap foremost john \
    && rm -rf /var/lib/apt/lists/

# Install python3 properly
RUN ln -s /bin/python3 /bin/python \
    && ln -s /usr/bin/pip3 /usr/bin/pip

# Install zsh
RUN /install.sh zsh.sh

# Install sqlmap
RUN /install.sh sqlmap.sh

# Install dirsearch
RUN /install.sh dirsearch.sh

# Download searchsploit but remove heavy local exploits
RUN /install.sh searchsploit.min.sh

# Install sherlock
RUN /install.sh sherlock.sh

# Install dog DNS tool
RUN /install.sh dog.sh

# Install arjun HTTP param fuzzer
RUN pip install arjun

# Install ffuf
RUN /install.sh ffuf.sh

# Add
#   mysql
#   Wordlists

WORKDIR "/root"