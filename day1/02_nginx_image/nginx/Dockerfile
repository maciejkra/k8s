FROM alpine
RUN apk add --update nginx && \
    rm -rf /var/cache/apk/* && \
    mkdir -p /tmp/nginx

COPY nginx.conf /etc/nginx/nginx.conf
COPY default.conf /etc/nginx/conf.d/default.conf
WORKDIR /usr/html
ENV MY_ENV_VARIABLE="SET ON WORKSHOPS"
COPY . ./
CMD nginx
