# Imagem oficial do Python 3.9 slim
FROM python:3.11-slim

# Define o diretório de trabalho dentro do container
WORKDIR /code

# Copia apenas os arquivos necessários para evitar carregar arquivos desnecessários
COPY requirements.txt /code/

# Instala as dependências diretamente do requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copia apenas o diretório 'app' para dentro do container
COPY . /code/app
