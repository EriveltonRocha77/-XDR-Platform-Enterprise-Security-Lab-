FROM python:3.11-alpine

WORKDIR /app

# Instala as dependências primeiro (melhor cache de build: só reinstala
# quando requirements.txt muda, não a cada alteração em main.py)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# O módulo cloud usa pyyaml, que já está listado em requirements.txt,
# então não é mais necessário instalá-lo separadamente.

COPY . /app/
