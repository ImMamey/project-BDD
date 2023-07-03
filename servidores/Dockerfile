# Servidor A
FROM python:3.10
WORKDIR /usr/app/src
VOLUME /data


COPY script.sh /usr/app/src/entrypoint.sh
COPY servidor_A.py .
COPY servidor_B.py .
COPY usuarios.db /data

RUN pip install pycryptodome==3.18.0
ENV PUERTO_A=5000
ENV PUERTO_B=5001
EXPOSE 5000/tcp
EXPOSE 5001/tcp


CMD ["/usr/app/src/entrypoint.sh"]