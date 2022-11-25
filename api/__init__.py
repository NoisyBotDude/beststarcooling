from fastapi import FastAPI
import asyncio
from logging import log
from os import environ, path
from fastapi.middleware.cors import CORSMiddleware

from pymongo import errors

from api.routes.user import (user_general_routes)
from api.config.database import database
from dotenv import load_dotenv

BASE_DIR = path.abspath(path.dirname(__file__))

def create_app():
    
    description = """
        Best Place to Get Repairing Services
    """

    # Initialize fastapi app
    app = FastAPI(
        title = "BestStarCooling",
        description = description
    )

    origins = ["*"]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.on_event("startup")
    async def startup_event():
        try:

            # Loading environment variables from environment file
            load_dotenv(path.join(BASE_DIR, '.env'))
            
            # Connect with database
            await asyncio.wait_for(database(), timeout=60.0)

        except asyncio.TimeoutError as e:
            #TODO: log error and continuous retry
            log("DB Timeout")
            pass

        except errors.DuplicateKeyError as e:
            #TODO: Critical error, notify to admin and dev
            log("DUPLICATE")

        except Exception as e:
            #TODO: Notify admin

            print("EXCEPTION", e)


    # Triggers functions on shutdown
    @app.on_event("shutdown")
    async def shutdown_event():
        print("SHUTDOWN")

    @app.get("/")
    async def index():
        return {"message" : "running"}

    app.include_router(
        user_general_routes.construct_router(),
        prefix = "/user"
    )

    return app
