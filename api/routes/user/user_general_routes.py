from api.schemas.user.request_schemas import user_request_schema
from fastapi import APIRouter, Depends, status
from api.models.user import user_model
from api.drivers.user import user_drivers
from api.utils.exceptions import exceptions

from fastapi.responses import JSONResponse, RedirectResponse
from passlib.hash import pbkdf2_sha256
import jwt
import datetime
from os import environ
from api.repository import user_repo
from fastapi import APIRouter, Depends, HTTPException, Request, status



def construct_router():
    
    user = APIRouter(
        tags=["User"]
    )

    @user.post("/login" , status_code=status.HTTP_200_OK)
    async def login(request: Request):
        """Handles student login."""

        try:
            request = await request.json()

            user = await user_model.UserModel.find_one(
                user_model.UserModel.email == request["email"]
            )

            if user is None:
                return JSONResponse(
                    status_code=500,
                    content = {
                        "message": "student doesn't exist"
                    }
                )

            if not pbkdf2_sha256.verify(request["password"], user.password):
                return JSONResponse(
                    status_code=403,
                    content={
                        "message" : "Username or password incorrect"
                    }
                )

            jwt_payload = jwt.encode(
                {
                    "token" : user.user_id,
                    "role" : "student",
                    "exp": datetime.datetime.now(tz=datetime.timezone.utc) + 
                            datetime.timedelta(days = int(environ.get("JWT_EXP", 1)))
                },
                environ.get("SECRET_KEY"),
                algorithm=environ.get("JWT_ALGORITHM")
            )

            response =await user_repo.update_refresh_token(user.user_id)

            if not response:
                return JSONResponse(
                    status_code=500,
                    content = {
                        "message" : "internal server error"
                    }
                )
            
            refresh_token = jwt.encode(
                {
                    "user_id" : user.user_id,
                    "role" : "student",
                    "refresh_token" : response,
                    "exp": datetime.datetime.now(tz=datetime.timezone.utc) + 
                            datetime.timedelta(days = int(environ.get("JWT_EXP", 1)))
                },
                environ.get("SECRET_KEY"),
                algorithm=environ.get("JWT_ALGORITHM")
            )

            return JSONResponse(
                status_code=200,
                content = {
                    "token" : jwt_payload,
                    "refresh_token" : refresh_token
                }
            )

        except Exception as e:
            return JSONResponse(
                status_code=500, 
                content = {
                    "message" : "internal server error"
                }
            )

    @user.post("/add")
    async def add_user(request: user_request_schema.UserRegisterSchema):
        #TODO: Optimise and clean the code
        try:

            student = user_drivers.User()

            response = await student.add_user(request)
            
            message = "student created"

            return JSONResponse(
                status_code=status.HTTP_201_CREATED, 
                content=message
            )

        except exceptions.UnexpectedError as e:
            #TODO: log to logger

            return JSONResponse(
                status_code=500,
                content="unexpected error occured"
            )

        except exceptions.DuplicateStudent as e:
            #TODO: log to logger

            return JSONResponse(
                status_code=409,
                content="student already exists"
            )

    return user
