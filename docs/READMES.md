<p align="center">
    <h1 align="center"> Distributed Systems Project</h1>
    <h4 align="center"><a href="docs/READMES.md">Readme en Español</a></h4>
</p>

## Desarrolladores
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
## Descripción

Este es un proyecto universitario para una arquitectura Cliente-Servidor, utilizando sockets TCP, subprocesos, contenedores docker y redes docker.
* Hay 2 servidores, que pueden acceder a una base de datos.
* Hay clientes que pueden solicitar alta, registro, verificación de identidad y encriptación de mensajes a estos servidores.
* Todas las conexiones ocurren a través de un servidor "proxy", que maneja todas las conexiones de los clientes a los 2 servidores.

Una explicación de la arquitectura de este programa sería el siguiente UML
<p align="center">
    <img src="images\uml.jpg" title="uml" width="450">
</p>

---
## Requisitos
* [Python 3.10](https://www.python.org/downloads/)
* [pycryptodome 3.18.0](https://pycryptodome.readthedocs.io/en/latest/src/installation.html)
* [Docker](https://docs.docker.com/engine/install/)
* [Poetry](https://python-poetry.org/) (Para el manejo de depenendencias y ambientes virtuales en el IDE)

> Si no desea usar poetry, deberás instalar todas las dependencias en `pyproject.toml` manualmente con pip install
# Como instalar / ejecutar
## Instalación en el IDE
1. Descarga el proyecto y accede a su directorio.
2. Ejecute `pip install poetry`
3. Ejecute `poetry install`
4. Una vez que la poetry cree el entorno virtual desde `pyproject.toml`, agréguelo como intérprete para su IDE.
## Ejecución en el IDE

​
118 / 5,000
Translation results
Translation result
Una vez que haya configurado todo y el proyecto instalado para ejecutar el proyecto, debe ejecutar estos archivos en orden:
1. `servidor_A.py` y `servidor_B.py`
2. `proxy.py`
3. `client.py`
> El orden de ejecución es importante, de lo contrario los sockets de cada archivo no se comunicarán.
## Ejecución en Docker
 Paso 1: Cree cada imagen con los siguientes comandos de terminal:
1. `cd cliente`
2. `sudo docker build -t imagen_cliente .`
3. `cd servidores`
4. `sudo docker build -t imagen_servidores .`
5. `cd proxy` 
6. `sudo docker build -t imagen_proxy .`

Paso 2: crea una red docker:
1. `docker network create red_sergio_hernani_victor`

Paso 3: Crea los contenedores con las imágenes y la red

1. `sudo docker run --name contenedor_servidores --network red_sergio_hernani_victor -d imagen_servidores`
2. `sudo docker run --name contenedor_proxy --network red_sergio_hernani_victor -p 127.0.0.1:6000:6000 -d imagen_proxy`
3. `sudo docker run -it --name contenedor_cliente --network red_sergio_hernani_victor imagen_cliente`

Con todos los pasos anteriores completados, debería poder interactuar con el contenedor con el cliente.

---
## Licencia
Lea el archivo [`LICENSE`](docs/LICENSE) para mas información.
