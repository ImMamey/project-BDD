# Proxy
FROM python:3.10
WORKDIR /usr/app/src
COPY . /

RUN pip install pycryptodome==3.18.0

# ports for "contenedor servidores"
ENV SERVIDORES=contenedor_servidores
ENV SERVIDOR_A_PUERTO=5000
ENV SERVIDOR_B_PUERTO=5001

ENV PROXY_PUERTO=6000
EXPOSE 6000/tcp


CMD ["python", "/proxy.py"]