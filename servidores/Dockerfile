# Servidor A
FROM python:3.10
WORKDIR /usr/app/src
VOLUME data

COPY ../servidores /
RUN pip install pycryptodome==3.18.0
ENV PUERTO_A=5000
ENV PUERTO_B=5001
EXPOSE 5000/tcp
EXPOSE 5001/tcp
COPY script.sh /entrypoint.sh


CMD ["/usr/app/src/entrypoint.sh"]