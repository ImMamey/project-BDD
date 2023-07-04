# Proxy
FROM python:3.10
WORKDIR /usr/app/src
COPY proxy.py .

RUN pip install pycryptodome==3.18.0

# ports for "contenedor servidores"
<<<<<<< Updated upstream
ENV SERVIDORES=contenedor_servidores
ENV CLIENTE=contenedor_cliente

ENV PROXY_PUERTO=6000
=======
ENV HOST_SERVIDORES=contenedor_servidores
>>>>>>> Stashed changes
EXPOSE 6000/tcp


CMD ["python", "/proxy.py"]