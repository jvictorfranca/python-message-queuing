FROM postgres:13

# Copiar script de inicialização para dentro do contêiner
COPY init.sql /docker-entrypoint-initdb.d/

# Expor a porta padrão do PostgreSQL
EXPOSE 5432
