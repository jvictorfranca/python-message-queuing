from fastapi import FastAPI, Depends
import aio_pika
import asyncio
import json
import os
import logging
from sqlalchemy.orm import Session
from app.database import get_session, Base, engine
from app.models import UserModel
from uuid import uuid4

# Logger configuration to record events and errors
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI()

# RabbitMQ configuration with credentials and host defined in environment variables
RABBITMQ_URL = f"amqp://{os.environ['RABBITMQ_USER']}:{os.environ['RABBITMQ_PASS']}@{os.environ['RABBITMQ_HOST']}/"
QUEUE_NAME = "messages"

async def process_incoming_message(message: aio_pika.IncomingMessage):
    """
    Processes messages received from the RabbitMQ queue.
    - Reads and acknowledges (ack) the message.
    - Decodes the JSON and extracts the user data.
    - Inserts the user into the database.
    """
    message.ack()  # Acknowledges receipt of the message
    body = message.body
    logger.info("Received message")

    if body:
        parsed_message = json.loads(body)
        created_user = parsed_message['user']

        # Gets a database session
        session: Session = next(get_session())
        try:
            # Creates a new user with the data from the message
            user_model = UserModel(
                id=created_user['id'],
                name=created_user['name'],
                email=created_user['email']
            )

            session.add(user_model)
            session.commit()
            logger.info(f"User {user_model.id} created successfully.")
        except Exception as e:
            session.rollback()
            logger.error(f"Error processing message: {str(e)}")
        finally:
            session.close()

        logger.info(f"Message content: {parsed_message}")

async def consume(loop):
    """
    Initializes the RabbitMQ message consumer.
    - Establishes a connection to RabbitMQ.
    - Declares the queue and starts listening for messages.
    - Calls 'process_incoming_message' when a new message arrives.
    """
    try:
        connection = await aio_pika.connect_robust(RABBITMQ_URL, loop=loop)
        channel = await connection.channel()
        queue = await channel.declare_queue(QUEUE_NAME)
        await queue.consume(process_incoming_message, no_ack=False)
        logger.info("Waiting for messages...")
        return connection
    except Exception as e:
        logger.error(f"Consumer error: {e}")

@app.get("/list_users")
async def list_users(session: Session = Depends(get_session)):
    """Returns the list of users registered in the database."""
    return session.query(UserModel).all()

@app.on_event("startup")
async def startup_event():
    """
    Executed when the service starts.
    - Creates the database tables if they do not already exist.
    - Starts the RabbitMQ message consumer in the background.
    """
    Base.metadata.create_all(bind=engine)
    logger.info("Tables created successfully.")

    # Gets the current event loop and starts consuming RabbitMQ messages
    loop = asyncio.get_running_loop()
    task = loop.create_task(consume(loop=loop))
    await task