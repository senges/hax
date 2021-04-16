FROM ubuntu:latest

ARG DEBIAN_FRONTEND=noninteractive

# Add install script
COPY ../../script/install.sh /install.sh
RUN chmod +x /install.sh

# Install common packages
RUN apt update

# RUN apt update \
#     && apt install -y --no-install-recommends wget gnupg2 \
#     && rm -rf /var/lib/apt/lists/

# Install metasploit
RUN /install.sh metasploit.sh