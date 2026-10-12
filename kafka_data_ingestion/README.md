# Ingestão de Dados

Este diretório demonstra o uso de filas em pipelines de ingestão e processamento de dados.

## Requisitos

Antes de iniciar, certifique-se de ter instalado em seu ambiente:

- **Docker**
- **Extensão do Docker para VS Code**

## Como Executar os Exemplos

1. Acesse a pasta do módulo:
   ```sh
   cd ingestao_dados
   ```
2. Inicie os containers com o Docker Compose:
   ```sh
   docker compose up -d
   ```
3. Para interromper a execução, utilize:
   ```sh
   docker compose down -v
   ```

### Endpoints Disponíveis

- **Kibana**: [http://localhost:5601](http://localhost:5601)
- **Kafka Control Center**: [http://localhost:9021](http://localhost:9021)

Caso não consiga acessar um endpoint usando `localhost`, tente `0.0.0.0` ou `127.0.0.1`.

### Acessando o Banco de Dados PostgreSQL

Para acessar o banco de dados dentro do container:

```sh
psql usuarios
```
