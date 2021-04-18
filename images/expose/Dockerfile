FROM pdrooo/hax:legacy

# Install ngrok
RUN /install.sh ngrok

ENTRYPOINT /tools/bin/ngrok tcp --authtoken $NGROK_TOK $NGROK_PORT