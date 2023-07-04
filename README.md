## COMO CORRER CON DOKCER
# Paso 1: Para crear cada imagen
1. Entrar en la carpeta "cliente" con "cd cliente" 
2. Correr en la terminal: `sudo docker build -t imagen_cliente .`
3. Entrar en la carpeta "servidores" con "cd servidores"
4. Correr en la terminal `sudo docker build -t imagen_servidores .`
5. Entrar en la carpeta "proxy" con "cd proxy"
6. Correr en la terminal: `sudo docker build -t imagen_proxy .`

## Paso 2: Luego creamos la red
* `docker network create red_sergio_hernani_victor`

## Paso 3: Creamos los contenedores con los siguientes comandos:

1. `sudo docker run --name contenedor_servidores --network red_sergio_hernani_victor -d imagen_servidores`

2. `sudo docker run --name contenedor_proxy --network red_sergio_hernani_victor -p 127.0.0.1:6000:6000 -d imagen_proxy`

3. `sudo docker run -it --name contenedor_cliente --network red_sergio_hernani_victor imagen_cliente`

## Paso 4: 
Con estos comandos ya daberian de estar todos los  contenedores activos, y el cliente deberia de funcionar

---

# Comandos opcionales
En el caso de necesitar ver logs de cada contenedor:
* `sudo docker logs contenedor_servidores`
* `sudo docker logs contenedor_proxy`
* `sudo docker logs contenedor_cliente`

En el caso de querer correr los contenedores despues de haberlos creado:
* `sudo docker start -i contenedor_cliente` (i es para iterativo)
* `sudo docker start contenedor_proxy`
* `sudor docker start contenedor_servidores`

Para ver las redes:
* `sudo docker network ls `

Para inspecionar que los contenedores esten funcionando en la red asignada (los contenedores deben de estar activos):
* `sudo docker network inspect red_sergio_hernani_victor`
