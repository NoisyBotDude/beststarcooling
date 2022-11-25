from api.schemas.user.request_schemas import user_request_schemas
from fastapi import APIRouter, Depends, status


def construct_router():
    
    user = APIRouter(
        tags=["User"]
    )