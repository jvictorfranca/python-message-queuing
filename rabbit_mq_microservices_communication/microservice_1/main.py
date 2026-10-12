from fastapi import FastAPI, Depends
import aio_pika
import json
import os
from sqlalchemy.orm import Session
from app.database import get_session, Base, engine
from app.models import UserModel
from uuid import uuid4
import logging

# Logger configuration to record application events
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI()

# RabbitMQ configuration with credentials and host defined in environment variables
RABBITMQ_URL = f"amqp://{os.environ['RABBITMQ_USER']}:{os.environ['RABBITMQ_PASS']}@{os.environ['RABBITMQ_HOST']}/"
QUEUE_NAME = "messages"

async def get_rabbit_connection():
    """
    Establishes and returns an asynchronous connection to RabbitMQ.
    This connection will be used to send messages to the queue.
    """
    return await aio_pika.connect_robust(RABBITMQ_URL)

@app.post("/send")
async def send_message(message: str):
    """
    Sends a message to the RabbitMQ queue.
    - Creates a connection to RabbitMQ.
    - Opens a communication channel.
    - Publishes the message to the specified queue.
    """
    connection = await get_rabbit_connection()
    async with connection:
        channel = await connection.channel()
        await channel.default_exchange.publish(
            aio_pika.Message(body=json.dumps({"message": message}).encode()),
            routing_key=QUEUE_NAME
        )
    return {"status": "Message sent"}

@app.post("/create_user")
async def create_user(name: str, email: str, password: str, session: Session = Depends(get_session)):
    """
    Creates a new user in the database and publishes the data to RabbitMQ.
    - Generates a UUID for the user.
    - Adds the user and commits the database transaction.
    - Rolls back the transaction if an error occurs.
    - Sends the user data to the RabbitMQ queue.
    """
    try:
        user_model = UserModel(
            id=uuid4(),
            name=name,
            email=email,
            password=password
        )
        session.add(user_model)
        session.commit()
    except Exception as e:
        session.rollback()
        logger.error(f"Error creating user: {e}")
        return {"error": str(e)}

    # Publishes the new user's data to RabbitMQ
    connection = await get_rabbit_connection()
    async with connection:
        channel = await connection.channel()
        await channel.default_exchange.publish(
            aio_pika.Message(body=json.dumps({
                "user": {
                    "id": str(user_model.id),
                    "name": user_model.name,
                    "email": user_model.email
                }
            }).encode()),
            routing_key=QUEUE_NAME
        )
    return {"message": "User created successfully."}

@app.get("/list_users")
async def list_users(session: Session = Depends(get_session)):
    """
    Returns a list of all users registered in the database.
    """
    return session.query(UserModel).all()

@app.on_event("startup")
async def startup_event():
    """
    Executed when the service starts.
    - Creates the database tables if they do not already exist.
    - Logs the operation.
    """
    Base.metadata.create_all(bind=engine)
    logger.info("Tables created successfully.")