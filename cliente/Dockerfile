# Cliente
FROM python:3.10
WORKDIR /usr/app/src
VOLUME /datos

COPY cliente.py .
COPY entrada.txt /datos
COPY salida.txt /datos

RUN pip install pycryptodome==3.18.0
# Establecer variables de entorno para la conexión

ENV SERVIDORES=contenedor_servidores
ENV PROXY=contenedor_proxy
ENV CLIENTE_PUERTO=6000
EXPOSE 6000/tcp


CMD ["python", "/cliente.py"]
