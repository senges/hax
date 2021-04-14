FROM ubuntu:latest

# docker run --rm -h hax -it hax:latest

# Install common packages
RUN apt update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends tzdata \
    && apt install -y git wget curl zip python3 python3-pip vim iputils-ping netcat dnsutils tree \

    # Install PHP
    php-cli php-curl php-json php-zip \
    
    # Install cracking tools
    john \

    # Install useful CTF tools
    nmap foremost \
    
    && rm -rf /var/lib/apt/lists/

# Install python3 properly
RUN ln -s /bin/python3 /bin/python \
    && ln -s /usr/bin/pip3 /usr/bin/pip

# Install zsh using `zsh-in-docker`
RUN sh -c "$(wget -O- https://github.com/deluan/zsh-in-docker/releases/download/v1.1.1/zsh-in-docker.sh)" -- \
    -t afowler \
    -p git \ 
    -p zsh-z \
    -a 'alias vi="vim"' \
    -a 'PATH=$PATH:/tools/bin'

# Install zsh-z plugin
RUN git clone https://github.com/agkozak/zsh-z.git /root/.oh-my-zsh/custom/plugins/zsh-z

# Create tools folder
RUN mkdir -p /tools/bin

# Install sqlmap
RUN git clone --depth 1 https://github.com/sqlmapproject/sqlmap.git /tools/sqlmap \
    && rm -rf /tools/sqlmap/.??* /tools/sqlmap/doc \
    && ln -s /tools/sqlmap/sqlmap.py /tools/bin/sqlmap

# Install dirsearch
RUN git clone --depth 1 https://github.com/maurosoria/dirsearch.git /tools/dirsearch \
    && pip install -r /tools/dirsearch/requirements.txt \
    && rm -rf /tools/dirsearch/.??* \
    && ln -s /tools/dirsearch/dirsearch.py /tools/bin/dirsearch

# Install metasploit
RUN curl https://raw.githubusercontent.com/rapid7/metasploit-omnibus/master/config/templates/metasploit-framework-wrappers/msfupdate.erb > /tmp/msfinstall \
    && chmod 755 /tmp/msfinstall \
    && /tmp/msfinstall \
    && rm -f /tmp/msfinstall

# Download searchsploit but remove local exploits
RUN git clone --depth 1 https://github.com/offensive-security/exploitdb.git /tools/exploitdb \
    && rm -rf /tools/exploitdb/.git* /tools/exploitdb/exploits /tools/exploitdb/shellcodes /tools/exploitdb/*.md \
    && ln -s /tools/exploitdb/searchsploit /tools/bin/searchsploit

# searchsploit() {
#     echo 
#     if [[ "$#" -ge 2 && "$1" == "dl" ]]; then
#         wget "https://www.exploit-db.com/download/$2"
#     else
#         /tools/exploitdb/searchsploit "$1"
#     fi
# }

# Install sherlock
RUN git clone --depth 1 https://github.com/sherlock-project/sherlock.git /tmp/sherlock \
    && pip install -r /tmp/sherlock/requirements.txt \
    && mv /tmp/sherlock/sherlock /tools/sherlock \
    && ln -s /tools/sherlock/sherlock.py /tools/bin/sherlock \
    && chmod +x /tools/sherlock/sherlock.py \
    && rm -rf /tmp/sherlock

# Install dog DNS tool
RUN echo "deb http://packages.azlux.fr/debian/ buster main" | tee /etc/apt/sources.list.d/azlux.list \
    && wget -qO - https://azlux.fr/repo.gpg.key | apt-key add - \
    && apt update \
    && apt install dog

# Install arjun HTTP param fuzzer
RUN pip install arjun

# Install ffuf
RUN curl --silent "https://api.github.com/repos/ffuf/ffuf/releases/latest" | grep '"tag_name":' | sed -E 's/.*"v([^"]+)".*/\1/' \
    | xargs -I@ wget https://github.com/ffuf/ffuf/releases/download/v@/ffuf_@_linux_amd64.tar.gz -O /tmp/ffuf.tar.gz \
    && mkdir -p /tmp/ffuf \
    && tar -C /tmp/ffuf -xzvf /tmp/ffuf.tar.gz \
    && mv /tmp/ffuf/ffuf /tools/bin/ffuf \
    && rm -rf /tmp/ffuf*

# Add :
#   searchsploit

# Optionnale
#   Hashcat

# Wordlists : mount volume /usr/share/wordlists

# groupadd -r mysql && useradd -r -g mysql mysql

# debconf: delaying package configuration, since apt-utils is not installed


# [WARNING]: Empty continuation line found in:
#     RUN apt update     && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends tzdata     && apt install -y git wget curl zip python3 python3-pip vim iputils-ping netcat dnsutils     php-cli php-curl php-json php-zip     john hashcat     nmap foremost     && rm -rf /var/lib/apt/lists/
# [WARNING]: Empty continuation lines will become errors in a future release.

WORKDIR "/root"

# ENTRYPOINT [ "/bin/zsh" ]