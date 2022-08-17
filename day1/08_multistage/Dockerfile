FROM gradle:4.10.2-jdk8
USER root
RUN mkdir -p /app
WORKDIR /app
COPY build.gradle ./
ADD src ./src
RUN gradle build
EXPOSE 8080/tcp
ENTRYPOINT [ "java", "-jar", "/app/build/libs/gs-spring-boot-docker-0.1.0.jar"]
