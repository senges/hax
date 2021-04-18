FROM hax-legacy:latest

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

# Install samdump2
RUN /install.sh samdump2

ENTRYPOINT [ "/bin/zsh" ]