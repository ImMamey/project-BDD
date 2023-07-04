# Cliente
FROM python:3.10
WORKDIR /usr/app/src
VOLUME /datos

COPY cliente.py .
COPY entrada.txt /datos/entrada.txt
COPY salida.txt /datos/salida.txt

RUN pip install pycryptodome==3.18.0
# Establecer variables de entorno para la conexión

ENV HOST_PROXY=contenedor_proxy
EXPOSE 6000/tcp



CMD ["python", "/usr/app/src/cliente.py"]
