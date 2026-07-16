FROM alpine
RUN apk add --no-cache curl jq && \
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl" && \
chmod u+x kubectl && mv kubectl /bin/kubectl
COPY operator.sh /usr/local/bin/operator.sh
RUN chmod 755  /usr/local/bin/operator.sh
CMD ["/usr/local/bin/operator.sh"]




