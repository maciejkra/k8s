FROM alpine
RUN apk add --no-cache curl jq && \
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl" && \
chmod u+x kubectl && mv kubectl /bin/kubectl

CMD ["/bin/kubectl","get","pods"]
