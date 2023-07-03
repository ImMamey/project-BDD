FROM python:3.10

WORKDIR . /
RUN apt-get update && apt-get install -y python3
RUN pip install pycryptodome==3.18.0

COPY . /
COPY entrada.txt /usr/app/src/entrada.txt
COPY salida.txt /usr/app/src/salida.txt
COPY usuarios.db /usr/app/src/usuarios.db
RUN ls -l
RUN pwd

# Puertos en los que se ejecuta la aplicación
EXPOSE 5000
EXPOSE 5001

CMD ["python", "-m", "servidor_a"]
CMD ["python", "-m", "servidor_b"]
CMD ["python", "-m", "proxy"]
CMD ["python", "-m", "cliente"]