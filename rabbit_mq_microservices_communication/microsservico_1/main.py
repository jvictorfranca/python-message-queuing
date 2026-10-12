from fastapi import FastAPI, Depends
import aio_pika
import json
import os
from sqlalchemy.orm import Session
from app.database import get_session, Base, engine
from app.models import UsuarioModel
from uuid import uuid4
import logging

# Configuração do logger para registrar eventos da aplicação
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI()

# Configuração do RabbitMQ com credenciais e host definidos nas variáveis de ambiente
RABBITMQ_URL = f"amqp://{os.environ['RABBITMQ_USER']}:{os.environ['RABBITMQ_PASS']}@{os.environ['RABBITMQ_HOST']}/"
QUEUE_NAME = "mensagens"

async def get_rabbit_connection():
    """
    Estabelece e retorna uma conexão assíncrona com o RabbitMQ.
    Essa conexão será usada para enviar mensagens para a fila.
    """
    return await aio_pika.connect_robust(RABBITMQ_URL)

@app.post("/send")
async def send_message(message: str):
    """
    Envia uma mensagem para a fila do RabbitMQ.
    - Cria uma conexão com o RabbitMQ.
    - Abre um canal de comunicação.
    - Publica a mensagem na fila definida.
    """
    connection = await get_rabbit_connection()
    async with connection:
        channel = await connection.channel()
        await channel.default_exchange.publish(
            aio_pika.Message(body=json.dumps({"message": message}).encode()),
            routing_key=QUEUE_NAME
        )
    return {"status": "Message sent"}

@app.post("/criar_usuario")
async def criar_usuario(nome: str, email: str, password: str, session: Session = Depends(get_session)):
    """
    Cria um novo usuário no banco de dados e publica os dados no RabbitMQ.
    - Gera um UUID para o usuário.
    - Adiciona e confirma a transação no banco de dados.
    - Caso ocorra erro, faz rollback da transação.
    - Envia os dados do usuário para a fila do RabbitMQ.
    """
    try:
        user_model = UsuarioModel(id=uuid4(), nome=nome, email=email, password=password)
        session.add(user_model)
        session.commit()
    except Exception as e:
        session.rollback()
        return {"error": str(e)}
    
    # Publica os dados do novo usuário no RabbitMQ
    connection = await get_rabbit_connection()
    async with connection:
        channel = await connection.channel()
        await channel.default_exchange.publish(
            aio_pika.Message(body=json.dumps({
                "usuario": {
                    "id": str(user_model.id),
                    "nome": user_model.nome,
                    "email": user_model.email
                }
            }).encode()),
            routing_key=QUEUE_NAME
        )
    return {"mensagem": "Usuário criado com sucesso."}

@app.get("/listar_usuarios")
async def listar_usuarios(session: Session = Depends(get_session)):
    """
    Retorna a lista de todos os usuários cadastrados no banco de dados.
    """
    return session.query(UsuarioModel).all()

@app.on_event("startup")
async def startup_event():
    """
    Executado na inicialização do serviço.
    - Cria as tabelas no banco de dados caso ainda não existam.
    - Registra a ação no log.
    """
    Base.metadata.create_all(bind=engine)
    logger.info("Tabelas criadas com sucesso.")
