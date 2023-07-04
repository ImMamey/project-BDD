# Proxy
FROM python:3.10
WORKDIR /usr/app/src
COPY proxy.py .

RUN pip install pycryptodome==3.18.0

# ports for "contenedor servidores"
ENV HOST_SERVIDORES=contenedor_servidores
EXPOSE 6000/tcp


CMD ["python", "/usr/app/src/proxy.py"]