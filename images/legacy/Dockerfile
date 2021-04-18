# +-------------------------------------------------+ #
# | THIS IMAGE IS THE BASE IMAGE FOR ALL OTHER      | #
# | HAX IMAGES. USE IT TO BUILD YOUR OWN HAX IMAGE. | #
# +-------------------------------------------------+ #

FROM ubuntu:latest

# Set command prefix as non interactive
ARG DEBIAN_FRONTEND=noninteractive

# Create tools folder
RUN mkdir -p /tools/bin

# Add install script
COPY ./scripts/install.sh /install.sh
RUN chmod +x /install.sh

# Install common packages
RUN apt update \
    && apt install -y --no-install-recommends tzdata git wget curl zip unzip vim iputils-ping netcat dnsutils tree whois

WORKDIR "/root"