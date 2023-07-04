# Cliente
FROM python:3.10
WORKDIR /usr/app/src
VOLUME /datos

COPY cliente.py .
COPY entrada.txt /datos/entrada.txt
COPY salida.txt /datos/salida.txt

RUN pip install pycryptodome==3.18.0
# Establecer variables de entorno para la conexión

<<<<<<< Updated upstream
ENV SERVIDORES=contenedor_servidores
ENV PROXY=contenedor_proxy
=======
ENV HOST_PROXY=contenedor_proxy
EXPOSE 6000/tcp
>>>>>>> Stashed changes


CMD ["python", "/cliente.py"]
