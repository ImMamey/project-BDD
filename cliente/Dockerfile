# Cliente
FROM python:3.10
WORKDIR . /
COPY . /
COPY cliente.py .
COPY entrada.txt .
COPY salida.txt .
RUN pip install pycryptodome==3.18.0
# Establecer variables de entorno para la conexión
ENV SERVIDOR_A_HOST=contenedor_servidor_a
ENV SERVIDOR_A_PUERTO=5000
ENV SERVIDOR_B_HOST=contenedor_servidor_b
ENV SERVIDOR_B_PUERTO=5001
ENV PROXY_HOST=proxy
ENV PROXY_PUERTO=6000


CMD ["python", "/cliente.py"]
