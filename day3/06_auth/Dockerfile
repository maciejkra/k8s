FROM alpine
RUN apk add --no-cache curl jq && \
curl -LO https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl && \
chmod u+x kubectl && mv kubectl /bin/kubectl

CMD ["/bin/kubectl","get","pods"]
