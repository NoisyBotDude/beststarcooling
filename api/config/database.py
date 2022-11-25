import asyncio
from os import environ

import motor
from api.models.user.user_model import UserModel
from beanie import init_beanie


async def database():

    # Create Motor client
    client = motor.motor_asyncio.AsyncIOMotorClient(
        environ.get("DEV_DB_URI")
    )
    print(environ.get("DEV_DB_URI"))

    await init_beanie(
        database = client.beststarcooling,
        document_models = [
            UserModel,
        ]
    )
   