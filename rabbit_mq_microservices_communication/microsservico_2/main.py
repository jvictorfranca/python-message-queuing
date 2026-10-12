from fastapi import FastAPI, Depends
import aio_pika
import asyncio
import json
import os
import logging
from sqlalchemy.orm import Session
from app.database import get_session, Base, engine
from app.models import UsuarioModel
from uuid import uuid4

# Configuração do logger para registrar eventos e erros
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI()

# Configuração do RabbitMQ com credenciais e host definidos nas variáveis de ambiente
RABBITMQ_URL = f"amqp://{os.environ['RABBITMQ_USER']}:{os.environ['RABBITMQ_PASS']}@{os.environ['RABBITMQ_HOST']}/"
QUEUE_NAME = "mensagens"

async def process_incoming_message(message: aio_pika.IncomingMessage):
    """
    Processa mensagens recebidas da fila do RabbitMQ.
    - Faz a leitura e o reconhecimento (ack) da mensagem.
    - Decodifica o JSON e extrai os dados do usuário.
    - Insere o usuário no banco de dados.
    """
    message.ack()  # Confirma o recebimento da mensagem
    body = message.body
    logger.info("Received message")

    if body:
        parsed_message = json.loads(body)
        created_user = parsed_message['usuario']

        # Obtém uma sessão do banco de dados
        session: Session = next(get_session())  
        try:
            # Cria um novo usuário com os dados da mensagem
            user_model = UsuarioModel(
                id=created_user['id'],
                nome=created_user['nome'],
                email=created_user['email']
            )
            
            session.add(user_model)
            session.commit()
            logger.info(f"Usuário {user_model.id} criado com sucesso.")
        except Exception as e:
            session.rollback()
            logger.error(f"Erro ao processar mensagem: {str(e)}")
        finally:
            session.close()
        
        logger.info(f"Message content: {parsed_message}")

async def consume(loop):
    """
    Inicializa o consumidor de mensagens do RabbitMQ.
    - Estabelece a conexão com o RabbitMQ.
    - Declara a fila e começa a escutar mensagens.
    - Chama 'process_incoming_message' ao receber uma nova mensagem.
    """
    try:
        connection = await aio_pika.connect_robust(RABBITMQ_URL, loop=loop)
        channel = await connection.channel()
        queue = await channel.declare_queue(QUEUE_NAME)
        await queue.consume(process_incoming_message, no_ack=False)
        logger.info("Waiting for messages...")
        return connection
    except Exception as e:
        logger.error(f"Erro no consumidor: {e}")

@app.get("/listar_usuarios")
async def listar_usuarios(session: Session = Depends(get_session)):
    """ Retorna a lista de usuários cadastrados no banco de dados. """
    return session.query(UsuarioModel).all()

@app.on_event("startup")
async def startup_event():
    """
    Executado na inicialização do serviço.
    - Cria as tabelas no banco de dados se ainda não existirem.
    - Inicia o consumidor de mensagens do RabbitMQ em segundo plano.
    """
    Base.metadata.create_all(bind=engine)
    logger.info("Tabelas criadas com sucesso.")

    # Obtém o loop de eventos atual e inicia o consumo de mensagens do RabbitMQ
    loop = asyncio.get_running_loop()
    task = loop.create_task(consume(loop=loop))
    await task
