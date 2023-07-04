<p align="center">
    <h1 align="center"> Distributed Systems Project</h1>
    <h4 align="center"><a href="docs/READMES.md">Readme en Español</a></h4>
</p>

## Developers
<table>
    <tbody>
        <tr>
            <td align="center"><a href="https://github.com/ImMamey" rel="nofollow"><img src="https://avatars.githubusercontent.com/u/32584037?v=4" width="150px;" alt="" style="max-width:100%;"><br><sub><b>Mamey</b></sub></a><br><a href="https://github.com/ImMamey/project-BDD/commits?author=ImMamey" title="Commits"><g-emoji class="g-emoji" alias="book" fallback-src="https://github.githubassets.com/images/icons/emoji/unicode/1f4d6.png">📖</g-emoji></a></td>
            <td align="center"><a href="https://github.com/heralex98" rel="nofollow"><img src="https://avatars.githubusercontent.com/u/106991487?v=4" width="150px;" alt="" style="max-width:100%;"><br><sub><b>Heralex</b></sub></a><br><a href="https://github.com/ImMamey/project-BDD/commits?author=ImMamey" title="Commits"><g-emoji class="g-emoji" alias="book" fallback-src="https://github.githubassets.com/images/icons/emoji/unicode/1f4d6.png">📖</g-emoji></a></td>
            <td align="center"><a href="https://github.com/ImMamey" rel="nofollow"><img src="https://avatars.githubusercontent.com/u/45183215?v=4" width="150px;" alt="" style="max-width:100%;"><br><sub><b>SergioRamirez</b></sub></a><br><a href="https://github.com/ImMamey/project-BDD/commits?author=ImMamey" title="Commits"><g-emoji class="g-emoji" alias="book" fallback-src="https://github.githubassets.com/images/icons/emoji/unicode/1f4d6.png">📖</g-emoji></a></td>
        </tr>
    </tbody>
</table>

---
## Description

This is an university project for a Client-Server architecture, using TCP sockets, threading, md5-hash encryption, docker containers and docker networking.
* There are 2 servers, that can access a database.
* There are clients that can request to sign up, register, identity verification, and encryption of  messages to these servers.
* All the connections happen through a "proxy" server, that handle all clients connections to the 2 servers.

An explanation of the architecture of this program would be the following UML (in spanish):
<p align="center">
    <img src="docs\images\uml.jpg" title="uml" width="450">
</p>

---
## Requirements
* [Python 3.10](https://www.python.org/downloads/)
* [pycryptodome 3.18.0](https://pycryptodome.readthedocs.io/en/latest/src/installation.html)
* [Docker](https://docs.docker.com/engine/install/)
* [Poetry](https://python-poetry.org/) (For dependency and venv management on the IDE)

> If you dont want to use poetry, you would need to install all the dependencies in the `pyproject.toml` manually with pip install
# How to install / run
## Installing on an IDE
1. Download the project and enter its directory.
2. Run pip install poetry
3. Run poetry install
4. Once poetry creates the virtual environment from the `pyproject.toml` add it as an interpreter for your IDE.

## Running on an IDE
Once you have everything set up and the project installed to run the project you need to execute these files in order:
1. `servidor_A.py` and `servidor_B.py`
2. `proxy.py`
3. `client.py`
> Execution order is important, otherwise the sockets of each file wont communicate.
## Running on docker
 Step 1: Create each image with the following terminal commands:
1. `cd cliente`
2. `sudo docker build -t imagen_cliente .`
3. `cd servidores`
4. `sudo docker build -t imagen_servidores .`
5. `cd proxy` 
6. `sudo docker build -t imagen_proxy .`

Step 2: create a docker network:
1. `docker network create red_sergio_hernani_victor`

Step 3: Create the containers with the images and the network

1. `sudo docker run --name contenedor_servidores --network red_sergio_hernani_victor -d imagen_servidores`
2. `sudo docker run --name contenedor_proxy --network red_sergio_hernani_victor -p 127.0.0.1:6000:6000 -d imagen_proxy`
3. `sudo docker run -it --name contenedor_cliente --network red_sergio_hernani_victor imagen_cliente`

With all the previous steps completed you can should be able to interact with the container with the client.

---
## License
Read the [`LICENSE`](docs/LICENSE) for more info,
