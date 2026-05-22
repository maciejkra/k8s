# CI/CD - Jenkins

Build Images
```sh 
docker build -t myjenkins -f Dockerfile.jenkins .
docker build -t krajewskim/kubectl -f Dockerfile.kubectl .
```

Lunch Jenkins
```sh
docker run -d --restart=always -p 8080:8080 --name jenkins -v jenkins:/var/jenkins_home -v /var/run/docker.sock:/var/run/docker.sock --privileged myjenkins
```

Install Jenkins plugins:
* Kubernetes CLI
* Docker Pipeline
