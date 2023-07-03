# Servidor B
FROM python:3.10
WORKDIR . /
COPY . /
COPY servidor_B.py .
RUN pip install pycryptodome==3.18.0
EXPOSE 5001

ENV PUERTO=5001
CMD ["python", "/servidor_B.py"]
