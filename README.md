# Convention

```
<command> - represents command
<command|command2> - represent possible commands
<?> - represents placeholder to be filled by task resolution
<??> - represents one or many placeholders to be filled 
# - represents comment, example
``` 

# k8's workshops

## Instalacja

<details><summary>Install Docker on Linux</summary>
<p>

```bash
# Install Docker
curl -fsSL https://get.docker.com | sh

# Install Docker w $HOME jako non-root
curl -fsSL https://get.docker.com/rootless | sh
```

</p>
</details>

<details><summary>Install Docker helpers</summary>
<p>

```bash
# Windows
$ Install-Module DockerCompletion -Scope CurrentUser
$ Import-Module DockerCompletion

# Mac
$ brew tap homebrew/completions
$ brew install docker-completion
$ brew install docker-compose-completion

# Linux
$ apt install bash-completion
$ curl https://raw.githubusercontent.com/docker/docker-ce/master/components/cli/contrib/completion/bash/docker -o /etc/bash_completion.d/docker.sh
```

</p>
</details>

Uruchomienie pierwszego kontenera :)
```
docker run hello-world
```

### Podstawowe komendy:

Sciagniecie obrazu
```
docker pull IMAGE
```

Wylistowanie obrazów
```
docker images
```

Uruchomienie obrazu
```
docker run -it IMAGE komenda
```

Wylistowanie kontenerow
```
docker ps
```

Podlaczenie sie do dzialajacego kontenera
```
docker exec -it CONTAINER bash
```

Kopiowanie danych
```
docker cp CONTAINER:SRC_PATH DEST_PATH
```

Przekierowanie portow
```
docker run -it -p 80:80 IMAGE
```

Budowanie obrazu
```
docker build -t NAZWA:tag .
```

<details><summary>Podgląd komunikacji z kontenerem</summary>
<p>

```bash
socat -d -d -t100 \
   -lf /dev/stdout \
   -v UNIX-LISTEN:/var/run/docker.debug,mode=777,reuseaddr,fork \
      UNIX-CONNECT:/var/run/docker.sock
```

```bash
DOCKER_HOST=unix:///var/run/docker.debug docker ps
```

</p>
</details>

<details><summary>Wysłanie rządania do docker engine</summary>
<p>

```bash
curl -sSf --unix-socket /var/run/docker.sock 0/containers/json
```

</p>
</details>

<details><summary>Wejście do maszyny wirtualnej linuxa</summary>
<p>

```bash
# Windows and Mac
docker run -it --rm --privileged --pid=host justincormack/nsenter1
```

</p>
</details>
