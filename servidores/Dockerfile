# Servidor A
FROM python:3.10
WORKDIR . /
COPY ../servidor_A /
COPY servidor_A.py .
RUN pip install pycryptodome==3.18.0
EXPOSE 5000
ENV PUERTO=5000


CMD ["python", "/servidor_A.py"]