# Official Python 3.11 slim image
FROM python:3.11-slim

# Sets the working directory inside the container
WORKDIR /code

# Copies only the necessary files to avoid including unnecessary files
COPY requirements.txt /code/

# Installs dependencies directly from requirements.txt
RUN pip install --upgrade pip setuptools wheel \
    && pip install --no-cache-dir -r requirements.txt

# Copies only the 'app' directory into the container
COPY . /code/app