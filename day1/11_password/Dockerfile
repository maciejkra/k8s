FROM busybox
COPY password /
RUN rm /password
ENTRYPOINT [ "cat", "/password" ]