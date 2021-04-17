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

# Install python3
RUN /install.sh python3

# Install zsh
RUN /install.sh zsh

# Install john
RUN /install.sh john

# Install hashcat
RUN /install.sh hashcat

# Install fcrackzip
RUN /install.sh fcrackzip

# Install pydictor
RUN /install.sh pydictor

# Install cupp
RUN /install.sh cupp

WORKDIR "/root"