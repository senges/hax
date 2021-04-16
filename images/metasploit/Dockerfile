FROM ubuntu:latest

ARG DEBIAN_FRONTEND=noninteractive

# Add install script
COPY ./scripts/install.sh /install.sh
RUN chmod +x /install.sh

# Install common packages
RUN apt update \
    && apt install -y --no-install-recommends tzdata curl wget git

# RUN apt update \
#     && apt install -y --no-install-recommends wget gnupg2 \
#     && rm -rf /var/lib/apt/lists/

# Install metasploit
RUN /install.sh metasploit