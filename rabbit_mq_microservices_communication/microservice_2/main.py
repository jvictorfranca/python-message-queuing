from fastapi import FastAPI, Depends
import aio_pika
import asyncio
import json
import os
import logging
from sqlalchemy.orm import Session
from app.database import get_session, Base, engine
from app.models import UserModel

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
    - Decodes the JSON message and extracts the user data.
    - Inserts the user into the database.
    - Acknowledges the message after successful processing.
    """
    logger.info("Received message")

    async with message.process():
        if not message.body:
            logger.warning("Received an empty message")
            return

        parsed_message = json.loads(message.body)
        created_user = parsed_message["user"]

        # Gets a database session
        session_generator = get_session()
        session: Session = next(session_generator)

        try:
            # Creates a new user with the data from the message
            user_model = UserModel(
                id=created_user["id"],
                name=created_user["name"],
                email=created_user["email"],
            )

            session.add(user_model)
            session.commit()

            logger.info("User %s created successfully.", user_model.id)
            logger.info("Message content: %s", parsed_message)

        except Exception as e:
            session.rollback()
            logger.error("Error processing message: %s", e)
            raise

        finally:
            session.close()
            session_generator.close()

async def consume():
    """
    Initializes the RabbitMQ message consumer.
    - Establishes a connection to RabbitMQ.
    - Declares the queue and starts listening for messages.
    - Calls 'process_incoming_message' when a new message arrives.
    """
    try:
        connection = await aio_pika.connect_robust(RABBITMQ_URL)
        channel = await connection.channel()
        queue = await channel.declare_queue(QUEUE_NAME, durable=True)

        await queue.consume(process_incoming_message, no_ack=False)
        logger.info("Waiting for messages...")

        return connection

    except Exception:
        logger.exception("Consumer error")
        raise

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

    # Starts the RabbitMQ consumer in the background
    app.state.rabbitmq_task = asyncio.create_task(consume())

@app.on_event("shutdown")
async def shutdown_event():
    """Closes the RabbitMQ consumer when the service shuts down."""
    task = getattr(app.state, "rabbitmq_task", None)

    if task:
        task.cancel()
        try:
            connection = await task
        except asyncio.CancelledError:
            connection = None
        except Exception:
            logger.exception("Error while shutting down the RabbitMQ consumer")
            connection = None

        if connection and not connection.is_closed:
            await connection.close()