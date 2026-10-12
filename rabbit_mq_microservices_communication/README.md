# Comunicação entre Microsserviços

Este diretório contém exemplos e práticas sobre o uso de filas para comunicação eficiente entre microsserviços.

## Requisitos

Antes de iniciar, certifique-se de ter instalado em seu ambiente:

- **Docker**
- **Extensão do Docker para VS Code**

## Como Executar os Exemplos

1. Acesse a pasta do módulo:
   ```sh
   cd comunicacao_microsservicos
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

- **Microsserviço 1 (API)**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **Microsserviço 2 (API)**: [http://localhost:9000/docs](http://localhost:9000/docs)
- **RabbitMQ**: [http://localhost:15672](http://localhost:15672)

Caso não consiga acessar um endpoint usando `localhost`, tente `0.0.0.0` ou `127.0.0.1`.

### Variáveis de Ambiente

As seguintes variáveis de ambiente devem ser configuradas para o funcionamento adequado do sistema:

```sh
RABBITMQ_USER=admin
RABBITMQ_PASS=pass
```

Se houver detalhes adicionais sobre os exemplos, eles estarão incluídos nos arquivos correspondentes dentro desta pasta.

---
